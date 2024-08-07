from django.shortcuts import render

# Create your views here.


# Home view
def home(request):
    if request.method == 'GET':
        return render(request, 'appointment/home.html')
    


# Appointments views
def student(request):
    if request.method == 'GET':
        return render(request, 'appointment/student.html')
    


def employee(request):
    if request.method == 'GET':
        return render(request, 'appointment/employee.html')
    

def visitor(request):
    if request.method == 'GET':
        return render(request, 'appointment/visitor.html')