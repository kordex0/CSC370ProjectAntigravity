# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0003_auto_20151129_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='section',
            field=models.ForeignKey(to='courses.Section', related_name='assignments'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='assignment',
            field=models.ForeignKey(to='assignments.Assignment', related_name='submissions'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='students',
            field=models.ManyToManyField(to='users.User', related_name='submissions'),
        ),
    ]
