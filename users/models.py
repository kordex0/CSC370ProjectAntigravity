from django.db import models

from django.contrib.auth.models import User as DjangoUser

from django.core.exceptions import ValidationError


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
    
    def __str__(self):
        return self.django_user.first_name + " " + self.django_user.last_name

    def get_role_display(self):
        return self.ROLE_CHOICES[self.role][1]

def validate_admin(user):
    if user.role != User.ADMIN:
        raise ValidationError("User must be an admin");

def validate_teacher(user):
    if user.role != User.TEACHER:
        raise ValidationError("User must be a teacher");

def validate_student(user):
    if user.role != User.STUDENT:
        raise ValidationError("User must be a student");

