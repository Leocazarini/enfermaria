from django.urls import path
from .views import create_multiple_students, search_student

urlpatterns = [
    path('students/create-multiple/', create_multiple_students, name='create_multiple_students'),
    path('students/search/', search_student, name='search_student'),
    
]