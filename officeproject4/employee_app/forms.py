
from django import forms
from django.core.exceptions import ValidationError

from .models import Employee, Task, Attendance, LeaveRequest


class EmployeeForm(forms.ModelForm):
    class Meta:
        model=Employee
        fields=['first_name','last_name','dept','salary','bonus','role','phone','hire_date']
        widgets={
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'dept': forms.Select(attrs={'class': 'form-control'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'bonus': forms.NumberInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control'}),
            'hire_date': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),

            }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),



        }

class TaskSubmissionForm(forms.ModelForm):
    file = forms.FileField(required=False)

    class Meta:
        model = Task
        fields = ['file']
        widgets = {

            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file:
            raise ValidationError("This field is required.")
        return file

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['date', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.TextInput(attrs={'class': 'form-control'}),

        }



class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['start_date', 'end_date', 'reason']
        widgets = {
            # 'employee':forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),

        }
