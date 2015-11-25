from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
   
class Section(models.Model):
    name = models.CharField(max_length=255)
    course = models.ForeignKey('Course', related_name='sections')
    teacher = models.ForeignKey('users.Teacher', blank=True, null=True)
    students = models.ManyToManyField('users.Student', blank=True)
    
    def __str__(self):
        return self.course.name + " " + self.name
