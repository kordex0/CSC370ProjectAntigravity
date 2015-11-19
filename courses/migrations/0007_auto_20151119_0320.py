# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20151017_2119'),
        ('courses', '0006_auto_20151017_2129'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='students',
        ),
        migrations.AddField(
            model_name='section',
            name='students',
            field=models.ManyToManyField(blank=True, to='users.Student'),
        ),
    ]
