# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='teacher',
            field=models.ForeignKey(to='users.Teacher', default=''),
            preserve_default=False,
        ),
    ]
