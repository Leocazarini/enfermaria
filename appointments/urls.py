from django.urls import path, include
from . import views

urlpatterns = [ 
    path('home/', views.home, name='home'),

    path('student/', views.student_appointment, name='student'),
    path('employee/', views.employee_appointment, name='employee'),

    path('visitor/', views.visitor_appointment, name='visitor'),
]
