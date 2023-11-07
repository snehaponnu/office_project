from django.contrib import messages
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404

from .forms import EmployeeForm, TaskForm, TaskSubmissionForm, AttendanceForm, LeaveRequestForm
from .models import *


# Create your views here.
def index(request):
    return render(request, 'index.html')


def admin_login(request):
    if request.method == 'POST':
        username1 = request.POST['username']
        password1 = request.POST['password']
        user = auth.authenticate(username=username1, password=password1)
        if user is not None and user.is_staff:
            auth.login(request, user)
            return redirect('admin_home')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('admin_login')
    return render(request, 'admin_login.html')


def admin_home(request):
    return render(request, 'admin_home.html')

def add_department(request):
    if request.method=='POST':
        department=request.POST['department']
        location = request.POST['location']
        new_dep=Department(department=department,location=location)
        new_dep.save()
        messages.success(request, 'Add Department successfully')
        return redirect('add_department')

    return render(request, 'add_department.html')


def add_role(request):
    departments = Department.objects.all()  # Fetch all departments
    if request.method == 'POST':
        role = request.POST['role']
        selected_department_id = request.POST.get('department')  # Get the selected department ID

        try:
            selected_department = Department.objects.get(pk=selected_department_id)
        except Department.DoesNotExist:
            selected_department = None

        if selected_department:
            new_role = Role(role=role, dept=selected_department)
            new_role.save()

            messages.success(request, 'Role added successfully')
            return redirect('add_role')
        else:
            messages.error(request, 'Invalid department selected')

    return render(request, 'add_role.html', {'departments': departments})


def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'employee added successfully')
            return redirect('add_employee')
    else:
        form = EmployeeForm()
        # messages.success(request, 'something went wrong')
    return render(request, 'add_employee.html', {'form': form})

def view_employee(request):
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    print(context)
    return render(request, 'view_employee.html', context)


def edit_employee(request,emp_id):
    employee = Employee.objects.get(id=emp_id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'employee edited successfully')
            return redirect('view_employee')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'edit_employee.html', {'form': form})


def delete_employee(request,emp_id):
        if request.method == 'POST':
            employee =Employee.objects.get(id=emp_id)
            employee.delete()
            messages.success(request, 'employee deleted successfully')
            return redirect('view_employee')
        return render(request, 'remove.html')


def registration(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        if password == password1:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('registration')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'email Taken')
                return redirect('registration')
            else:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username,
                                                email=email, password=password)
                user.save();
                messages.info(request, 'Successfully Registered')
                return redirect('emp_login')
        else:
            messages.info(request, 'password not matched')
            return redirect('registration')
        return redirect('/')

    return render(request, 'register.html')


def emp_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            request.session['username'] = username
            return redirect('employee_home')
        else:
            messages.info(request,'invalid credentials')
            return redirect('emp_login')
    return  render(request,'emp_login.html',{'username': request.session.get('username', '')})

def employee_home(request):
    return render(request, 'employee_home.html')


def employee_profile(request):
    employee = Employee.objects.first()  # You should retrieve the employee you want to display
    # employee = Employee.objects.get(id=emp_id)
    form = EmployeeForm(instance=employee)  # Pass the employee instance to the form
    return render(request, 'employee_profile.html', {'form': form, 'employee': employee})


def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'task assigned successfully')
            return redirect('add_task')  # Redirect to the task list view (update the name if needed)
    else:
        form = TaskForm()

    return render(request, 'add_task.html', {'form': form})

def all_task(request):
    tasks = Task.objects.all()
    context = {'tasks': tasks}
    return render(request, 'admin_view_task.html', context)

def employee_task(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    # tasks = Task.objects.all()  # You should replace this with your actual query to fetch the tasks
    file_names = {task.id: task.file.name for task in tasks if task.file}  # Create a dictionary with task IDs and their associated file names
    return render(request, 'employee_view_task.html', {'tasks': tasks, 'file_names': file_names})



def employee_task_submission(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == 'POST':
        form = TaskSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            task.file = form.cleaned_data['file']
            task.save()
            messages.success(request, 'Task submitted successfully')
            # You can add additional logic here, e.g., sending notifications, updating the task status, etc.
            return redirect('employee_task_submission', task_id=task_id)  # Redirect to the task detail page
    else:
        form = TaskSubmissionForm()

    return render(request, 'employee_task_submission.html', {'form': form, 'task': task})


def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            employee = request.user

            # Check if attendance already marked for the given date
            existing_attendance = Attendance.objects.filter(employee=employee, date=date)

            if existing_attendance.exists():
                messages.error(request, 'Attendance has already been marked for this date.')
            else:
                attendance = form.save(commit=False)
                attendance.employee = employee
                attendance.save()
                messages.success(request, 'Attendance marked successfully')
                return redirect('mark_attendance')

    else:
        form = AttendanceForm()

    return render(request, 'mark_attendance.html', {'form': form})

def view_attendance(request):
    attendance_records = Attendance.objects.filter(employee=request.user)
    return render(request, 'view_attendance.html', {'attendance_records': attendance_records})


def admin_view_attendence(request):
        attendance_records = Attendance.objects.all()
        return render(request, 'admin_view_attendence.html', {'attendance_records': attendance_records})


def employee_apply_leave(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.employee = request.user
            leave_request.save()
            messages.success(request,'Leave application sent successfully')
            return redirect('employee_apply_leave')  # Redirect to a success page
    else:
        form = LeaveRequestForm()
    return render(request, 'employee_apply_leave.html', {'form': form})

def admin_leave_approval(request):
    leave_requests = LeaveRequest.objects.all()
    return render(request, 'admin_leave_approval.html', {'leave_requests': leave_requests})


def approve_leave(request, request_id):

        leave_request = get_object_or_404(LeaveRequest, pk=request_id)
        leave_request.status = 'Approved'
        leave_request.save()
        return redirect('admin_leave_approval')

def reject_leave(request, request_id):
        leave_request = get_object_or_404(LeaveRequest, pk=request_id)
        leave_request.status = 'Declined'
        leave_request.save()
        # messages.error(request, 'Leave request declined.')
        return redirect('admin_leave_approval')

def employee_leave_status(request):
    employee_leave_requests = LeaveRequest.objects.filter(employee=request.user)
    return render(request, 'employee_leave_status.html', {'employee_leave_requests': employee_leave_requests})


def logout(request):
    auth.logout(request)
    return redirect('/')