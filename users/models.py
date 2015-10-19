from django.db import models

from django.contrib.auth.models import User as DjangoUser


class User(models.Model):
    django_user = models.OneToOneField(DjangoUser)
    
    class Meta:
        abstract = True
    
    def __str__(self):
        return self.django_user.first_name + " " + self.django_user.last_name

class Admin(User):
    pass
   
class Teacher(User):
    pass
    
class Student(User):
    pass

