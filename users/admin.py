from django.contrib import admin

from .models import Admin, Teacher, Student

admin.site.register(Admin)
admin.site.register(Teacher)
admin.site.register(Student)
