from django.db import models

from users.models import validate_teacher, validate_student

class Course(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
   
class Section(models.Model):
    name = models.CharField(max_length=255)
    course = models.ForeignKey('Course', related_name='sections')
    teacher = models.ForeignKey('users.User', blank=True, null=True, validators=[validate_teacher], related_name="+")
    students = models.ManyToManyField('users.User', blank=True)
    
    def __str__(self):
        return self.course.name + " " + self.name
