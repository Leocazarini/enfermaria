from django.shortcuts import render
from django.http import HttpResponse
from . import models
from patients.models import Student, Employee, Visitor
from django.contrib.auth.decorators import login_required




# Home view

@login_required
def home(request):
    if request.method == 'GET':
        return render(request, 'appointment/home.html')
    







# Appointments views
def student(request):
    if request.method == 'GET':
        return render(request, 'appointment/student.html')
    
    if request.method == 'POST': 
        
        pass


def employee(request):
    if request.method == 'GET':
        return render(request, 'appointment/employee.html')
    










def visitor(request):
    if request.method == 'GET':
        return render(request, 'appointment/visitor.html')