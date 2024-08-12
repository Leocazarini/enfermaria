from django.db import models
from patients.models import *

# Create your models here.



# workspace indentifiers
class Infirmary(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)


    def __str__(self):
        return self.name
    

class Nurse(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    badge_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


# appointment models

class StudentAppointment(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    student_info = models.ForeignKey(StudentInfo, on_delete=models.CASCADE)
    infirmary = models.ForeignKey(Infirmary, on_delete=models.CASCADE)
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    date = models.DateTimeField()
    reason = models.TextField()
    treatment = models.TextField()
    notes = models.TextField(blank=True, null=True)
    revaluation = models.BooleanField(default=False)
    contact_parents = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.name} - {self.date}"

class EmployeeAppointment(models.Model):
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    employee_info = models.ForeignKey(EmployeeInfo, on_delete=models.CASCADE)
    infirmary = models.ForeignKey(Infirmary, on_delete=models.CASCADE)
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    date = models.DateTimeField()
    reason = models.TextField()
    treatment = models.TextField()
    notes = models.TextField(blank=True, null=True)
    revaluation = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee.name} - {self.date}"

class VisitorAppointment(models.Model):
    id = models.AutoField(primary_key=True)
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    infirmary = models.ForeignKey(Infirmary, on_delete=models.CASCADE)
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    date = models.DateTimeField()
    reason = models.TextField()
    treatment = models.TextField()
    notes = models.TextField(blank=True, null=True)
    revaluation = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.visitor.name} - {self.date}"