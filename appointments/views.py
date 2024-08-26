from django.shortcuts import render
from django.http import HttpResponse
from . import models
from patients.models import Student, Employee, Visitor
from patients.views import search_student, search_employee, search_visitor
from django.contrib.auth.decorators import login_required




# Home view

@login_required
def home(request):
    if request.method == 'GET':

        return render(request, 'index.html')
    


def student_identify(request):
    if request.method == 'GET':
        return render(request, 'search_student.html')
    

def employee_identify(request):
    if request.method == 'GET':
        return render(request, 'search_employee.html')
    

def visitor_identify(request):
    if request.method == 'GET':
        return render(request, 'search_visitor.html')

        

# Appointments views

@login_required
def student_appointment(request):
    if request.method == 'GET':
        name = request.GET.get('name', None)
        registry = request.GET.get('ra', None)
        student = search_student(name, registry)

        return render(request, 'ap_student.html', {'student': student})

    if request.method == 'POST':        
        pass



@login_required
def employee_appointment(request):
    if request.method == 'GET':
        name = request.GET.get('name', None)
        registry = request.GET.get('badge', None)
        employee = search_employee(name, registry)

        return render(request, 'ap_employee.html', {'employee': employee})

    if request.method == 'POST': 
        pass
    



@login_required
def visitor_appointment(request):
    if request.method == 'GET':
        name = request.GET.get('name', None)
        if name:
            visitor = search_visitor(name)

            return render(request, 'ap_visitor.html', {'visitor': visitor}) 
              
        return render(request, 'ap_visitor.html')
    
    if request.method == 'POST':
        pass