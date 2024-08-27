from django.urls import path, include
from . import views

urlpatterns = [ 
    path('student/', views.student_appointment, name='student_appointment'),
    path('student/search/', views.student_identify, name='student_identify'),

    path('employee/', views.employee_appointment, name='employee_appointment'),
    path('employee/search/', views.employee_identify, name='employee_identify'),

    path('visitor/', views.visitor_appointment, name='visitor_appointment'),
    path('visitor/search/', views.visitor_identify, name='visitor_identify'),
]
