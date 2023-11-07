
from . import views
from django.urls import path

urlpatterns = [
    path('',views.index,name='index'),
path('registration',views.registration,name='registration'),
path('emp_login',views.emp_login,name='emp_login'),
path('employee_home',views.employee_home,name='employee_home'),
path('admin_login',views.admin_login,name='admin_login'),
path('admin_home',views.admin_home,name='admin_home'),
path('add_department',views.add_department,name='add_department'),
path('add_role',views.add_role,name='add_role'),
path('add_employee',views.add_employee,name='add_employee'),
path('edit_employee',views.edit_employee,name='edit_employee'),
path('edit_employee/<int:emp_id>/',views.edit_employee,name='edit_employee'),
path('view_employee',views.view_employee,name='view_employee'),
path('delete_employee',views.delete_employee,name='delete_employee'),
path('delete_employee/<int:emp_id>/',views.delete_employee,name='delete_employee'),
path('employee_profile/', views.employee_profile, name='employee_profile'),
path('add_task/', views.add_task, name='add_task'),
path('all_task/', views.all_task, name='all_task'),
path('employee_task/', views.employee_task, name='employee_task'),
path('employee_task_submission/<int:task_id>/', views.employee_task_submission, name='employee_task_submission'),
path('mark_attendance/', views.mark_attendance, name='mark_attendance'),
path('view_attendance/', views.view_attendance, name='view_attendance'),
path('admin_view_attendence/', views.admin_view_attendence, name='admin_view_attendence'),
path('employee_apply_leave/', views.employee_apply_leave, name='employee_apply_leave'),
path('admin_leave_approval/', views.admin_leave_approval, name='admin_leave_approval'),
path('approve-leave/<int:request_id>/', views.approve_leave, name='approve_leave'),
path('reject-leave/<int:request_id>/', views.reject_leave, name='reject_leave'),
path('employee_leave_status/', views.employee_leave_status, name='employee_leave_status'),
path('logout/', views.logout, name='logout'),
    ]