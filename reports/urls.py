from django.urls import path
from .views import *



urlpatterns = [
    path('records/student/', student_record, name='student_record'),
    path('records/student/search/', student_search, name='student_search'),


]