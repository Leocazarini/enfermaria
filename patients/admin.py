from django.contrib import admin
from .models import Employee, Student, Visitor


# Register your models here.


admin.site.register(Employee)
admin.site.register(Student)
admin.site.register(Visitor) 

