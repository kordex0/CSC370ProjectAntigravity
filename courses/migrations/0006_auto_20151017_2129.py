# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_auto_20151017_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='teacher',
            field=models.ForeignKey(null=True, blank=True, to='users.Teacher'),
        ),
    ]
