from django.db import models

from django.contrib.auth.models import User as DjangoUser

from django.core.exceptions import ValidationError


class TeacherManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=User.TEACHER)

class StudentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=User.STUDENT)

class AdminManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=User.ADMIN)

class User(models.Model):
    ADMIN = 0
    TEACHER = 1
    STUDENT = 2
    ROLE_CHOICES = (
        (ADMIN, "Admin"),
        (TEACHER, "Teacher"),
        (STUDENT, "Student")
    )
    django_user = models.OneToOneField(DjangoUser, related_name="user")
    role = models.SmallIntegerField(choices=ROLE_CHOICES)

    teachers = TeacherManager() 
    admins = AdminManager() 
    students = StudentManager() 
    
    def __str__(self):
        return self.django_user.first_name + " " + self.django_user.last_name

    def get_role_display(self):
        return self.ROLE_CHOICES[self.role][1]

    def is_admin(self):
        return True if self.role == self.ADMIN else False

    def is_student(self):
        return True if self.role == self.STUDENT else False

    def is_teacher(self):
        return True if self.role == self.TEACHER else False

def validate_admin(user_id):
    user = User.objects.get(id=user_id)  
    if user.role != User.ADMIN:
        raise ValidationError("User must be an admin");

def validate_teacher(user_id):
    user = User.objects.get(id=user_id)  
    if user.role != User.TEACHER:
        raise ValidationError("User must be a teacher");

def validate_student(user_id):
    user = User.objects.get(id=user_id)  
    if user.role != User.STUDENT:
        raise ValidationError("User must be a student");

