from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from .models import Student
from controller.crud import create_multiple_objects
import json


@csrf_exempt
def create_multiple_students(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if isinstance(data, list):
                return create_multiple_objects(Student, data)
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid data format, expected a list of objects'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)



def search_student(request):
    name = request.GET.get('name', None)
    ra = request.GET.get('ra', None)

    if not name and not ra:
        return JsonResponse({'status': 'error', 'message': 'Name or RA must be provided'}, status=400)

    if name:
        students = Student.objects.filter(name__icontains=name)
    elif ra:
        students = Student.objects.filter(ra=ra)
    
    if not students.exists():
        return JsonResponse({'status': 'error', 'message': 'No records found'}, status=404)

    student_list = [model_to_dict(student) for student in students]
    return JsonResponse({'status': 'success', 'data': student_list}, status=200)