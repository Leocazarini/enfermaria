from django.urls import path
from .views import *
urlpatterns = [
    path('students/create/', create_students, name='create_students'),
    path('students/search/', search_student, name='search_student'),
    path('students/search/id/', search_student_by_id, name='search_student_by_id'),

    path('employees/create/', create_employees, name='create_employees'),
    path('employees/search/', search_employee, name='search_employee'),
    path('employees/search/id/', search_employee_by_id, name='search_employee_by_id'),

    path('visitors/create/', create_visitor, name='create_visitor'),
    path('visitors/search/', search_visitor, name='search_visitor'),
    path('visitors/search/id/', search_visitor_by_id, name='search_visitor_by_id'),
    
]