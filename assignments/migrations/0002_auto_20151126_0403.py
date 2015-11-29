# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.utils import timezone
from django.db import migrations, models


def create_assignments(apps, schema_editor):
    User = apps.get_registered_model('users', 'User')
    Section = apps.get_registered_model('courses', 'Section')
    Assignment = apps.get_registered_model('assignments', 'Assignment')
    Submission = apps.get_registered_model('assignments', 'Submission')
    
    sdent = User.objects.get(django_user__username='sdent')
    hsort = User.objects.get(django_user__username='hshort')
    afowl = User.objects.get(django_user__username='afowl')
    okoboi = User.objects.get(django_user__username='okoboi')
    csc360a01 = Section.objects.get(name="A01", course__name="CSC360")
    csc360a02 = Section.objects.get(name="A02", course__name="CSC360")
    csc361a01 = Section.objects.get(name="A01", course__name="CSC361")
    csc361a02 = Section.objects.get(name="A02", course__name="CSC361")
    csc370a01 = Section.objects.get(name="A01", course__name="CSC370")
    csc370a02 = Section.objects.get(name="A02", course__name="CSC370")
    
    #Assignments
    csc360a01_1 = Assignment(name="Assignment1", section=csc360a01, description="description", due_date=timezone.make_aware(datetime.datetime(2015, 10, 23), timezone.get_current_timezone()))
    csc360a01_1.save()
    csc360a01_2 = Assignment(name="Assignment2", section=csc360a01, description="description", due_date=timezone.make_aware(datetime.datetime(2015, 12, 6), timezone.get_current_timezone()))
    csc360a01_2.save()
    
    csc360a02_1 = Assignment(name="Assignment1", section=csc360a02, description="description", due_date=timezone.make_aware(datetime.datetime(2015, 11, 2), timezone.get_current_timezone()))
    csc360a02_1.save()
    csc360a02_2 = Assignment(name="Assignment2", section=csc360a02, description="description", due_date=timezone.make_aware(datetime.datetime(2015, 12, 9), timezone.get_current_timezone()))
    csc360a02_2.save()
    
    csc361a01_1 = Assignment(name="Assignment1", section=csc361a01, description="description", due_date=timezone.make_aware(datetime.datetime(2015, 11, 12), timezone.get_current_timezone()))
    csc361a01_1.save()
    
    csc361a02_1 = Assignment(name="Assignment1", section=csc361a02, description="description", due_date=timezone.make_aware(datetime.datetime(2015, 11, 15), timezone.get_current_timezone()))
    csc361a02_1.save()
    
    csc370a01_1 = Assignment(name="Assignment1", section=csc370a01, description="description", due_date=timezone.make_aware(datetime.datetime(2015, 12, 6), timezone.get_current_timezone()))
    csc370a01_1.save()
    
    csc370a02_1 = Assignment(name="Assignment1", section=csc370a02, description="description", due_date=timezone.make_aware(datetime.datetime(2015, 12, 7), timezone.get_current_timezone()))
    csc370a02_1.save()
    
    #Submissions
    submission = Submission(assignment=csc360a01_1)
    submission.save()
    submission.students.add(afowl)
    submission = Submission(assignment=csc360a01_1)
    submission.save()
    submission.students.add(sdent)
    
    submission = Submission(assignment=csc360a01_2)
    submission.save()
    submission.students.add(afowl)
    submission.students.add(sdent)
    
    submission = Submission(assignment=csc360a02_1)
    submission.save()
    submission.students.add(okoboi)
    
    submission = Submission(assignment=csc360a02_2)
    submission.save()
    submission.students.add(okoboi)
    
    submission = Submission(assignment=csc361a01_1)
    submission.save()
    submission.students.add(okoboi)
    
    submission = Submission(assignment=csc361a02_1)
    submission.save()
    submission.students.add(afowl)
    
    submission = Submission(assignment=csc370a01_1)
    submission.save()
    submission.students.add(afowl)
    submission.students.add(hsort)
    
    submission = Submission(assignment=csc370a02_1)
    submission.save()
    submission.students.add(okoboi)

class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0001_initial'),
        ('users', '0002_auto_20151126_0252'),
        ('courses', '0002_auto_20151126_0335'),
    ]

    operations = [
        migrations.RunPython(create_assignments),
    ]
