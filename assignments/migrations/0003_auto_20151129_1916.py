# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0002_auto_20151126_0403'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='submission',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='submission',
            name='submitted',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
