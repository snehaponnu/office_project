from django.db import models

# Create your models here.
import datetime

from django.contrib.auth.models import User
from django.db import models


class Department(models.Model):
    department = models.CharField(max_length=100, null=False)
    location = models.CharField(max_length=100, null=False)

    def __str__(self):
        return "%s" % (self.department)


class Role(models.Model):
    role = models.CharField(max_length=100, null=False)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % (self.role)


class Employee(models.Model):
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    salary = models.IntegerField(default=0)
    bonus = models.IntegerField(default=0)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    phone = models.IntegerField(default=0)
    hire_date = models.DateField(max_length=50)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    file = models.FileField(upload_to='gallery')

    def __str__(self):
        return self.title


class Attendance(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    # date = models.DateField(null=True, blank=True)
    date = models.DateField(default=datetime.date.today)
    status = models.CharField(max_length=10)  # 'Present', 'Absent', etc.

    def __str__(self):
        return "%s " % (self.employee)




class LeaveRequest(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, default='Pending')  # 'Pending', 'Approved', 'Rejected'

    def __str__(self):
        return f"Leave request for {self.employee.username} "









# Create your models here.
