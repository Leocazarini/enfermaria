from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def student_record(request):

    if request.method == 'GET':
        return render(request, 'student_search_record.html')
    

def student_search(request):
    
        if request.method == 'GET':
            return render(request, 'student_record.html')