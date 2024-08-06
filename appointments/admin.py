from django.contrib import admin
from .models import Infirmary, StudentAppointment, EmployeeAppointment, VisitorAppointment


# Register your models here.
admin.site.register(Infirmary)
admin.site.register(StudentAppointment)
admin.site.register(EmployeeAppointment)
admin.site.register(VisitorAppointment)