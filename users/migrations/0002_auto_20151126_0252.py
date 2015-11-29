# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.contrib.auth.hashers import make_password


def create_users(apps, schema_editor):
    DjangoUser = apps.get_registered_model('auth', 'User')
    User = apps.get_registered_model('users', 'User')

    # These are not real objets, therefore dont have the role constants
    ADMIN = 0
    TEACHER = 1
    STUDENT = 2

    #Admins
    duser = DjangoUser(username='admin', first_name='Admin', last_name='Admin', password=make_password('admin'), is_superuser=False, is_staff=False)
    duser.save()
    User(django_user=duser, role=ADMIN).save()

    #Teachers
    duser = DjangoUser(username='jweber', first_name='Jens', last_name='Weber', password=make_password('jweber'), is_superuser=False, is_staff=False)
    duser.save()
    User(django_user=duser, role=TEACHER).save()

    duser = DjangoUser(username='jpan', first_name='Jianping', last_name='Pan', password=make_password('jpan'), is_superuser=False, is_staff=False,)
    duser.save()
    User(django_user=duser, role=TEACHER).save()

    duser = DjangoUser(username='kwu', first_name='Kui', last_name='Wu', password=make_password('kwu'), is_superuser=False, is_staff=False,)
    duser.save()
    User(django_user=duser, role=TEACHER).save()

    #Students
    duser = DjangoUser(username='sdent', first_name='Stu', last_name='Dent', password=make_password('sdent'), is_superuser=False, is_staff=False,)
    duser.save()
    User(django_user=duser, role=STUDENT).save()

    duser = DjangoUser(username='hsort', first_name='Holly', last_name='Short', password=make_password('hsort'), is_superuser=False, is_staff=False,)
    duser.save()
    User(django_user=duser, role=STUDENT).save()

    duser = DjangoUser(username='afowl', first_name='Artemis', last_name='Fowl', password=make_password('afowl'), is_superuser=False, is_staff=False,)
    duser.save()
    User(django_user=duser, role=STUDENT).save()

    duser = DjangoUser(username='okoboi', first_name='Opal', last_name='Koboi', password=make_password('okoboi'), is_superuser=False, is_staff=False,)
    duser.save()
    User(django_user=duser, role=STUDENT).save()

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_users),
    ]

