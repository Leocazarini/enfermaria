from django.urls import path, include
from . import views

urlpatterns = [ 
    path('home/', views.home, name='home'),
    path('student/', views.student, name='student'),
    path('employee/', views.employee, name='employee'),
    path('visitor/', views.visitor, name='visitor'),
]
