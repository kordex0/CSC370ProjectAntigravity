# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('course', models.ForeignKey(related_name='sections', to='courses.Course')),
                ('students', models.ManyToManyField(blank=True, to='users.User')),
                ('teacher', models.ForeignKey(blank=True, null=True, validators=[users.models.validate_teacher], related_name='+', to='users.User')),
            ],
        ),
    ]
