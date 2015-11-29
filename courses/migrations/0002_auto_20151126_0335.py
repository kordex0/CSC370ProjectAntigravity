# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def create_courses(apps, schema_editor):
    User = apps.get_registered_model('users', 'User')
    Course = apps.get_registered_model('courses', 'Course')
    Section = apps.get_registered_model('courses', 'Section')
    
    jweber = User.objects.get(django_user__username='jweber')
    jpan = User.objects.get(django_user__username='jpan')
    kwu = User.objects.get(django_user__username='kwu')
    sdent = User.objects.get(django_user__username='sdent')
    hsort = User.objects.get(django_user__username='hshort')
    afowl = User.objects.get(django_user__username='afowl')
    okoboi = User.objects.get(django_user__username='okoboi')
    
    #Courses
    csc360 = Course(name="CSC360")
    csc360.save()
    
    csc361 = Course(name="CSC361")
    csc361.save()
    
    csc370 = Course(name="CSC370")
    csc370.save()
    
    #Sections
    section = Section(name="A01", course=csc360, teacher=kwu)
    section.save()
    section.students.add(afowl)
    section.students.add(sdent)
    
    section = Section(name="A02", course=csc360, teacher=kwu)
    section.save()
    section.students.add(okoboi)
    
    section = Section(name="A03", course=csc360)
    section.save()
    
    section = Section(name="A01", course=csc361, teacher=jpan)
    section.save()
    section.students.add(okoboi)
    section.students.add(sdent)
    
    section = Section(name="A02", course=csc361, teacher=jpan)
    section.save()
    section.students.add(afowl)
    
    section = Section(name="A01", course=csc370, teacher=jweber)
    section.save()
    section.students.add(afowl)
    section.students.add(hsort)
    
    section = Section(name="A02", course=csc370, teacher=jweber)
    section.save()
    section.students.add(okoboi)

class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
        ('users', '0002_auto_20151126_0252'),
    ]

    operations = [
        migrations.RunPython(create_courses),
    ]
