# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-10 20:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('serfa_panel', '0012_sensor_last_synchro'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor',
            name='is_premium',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sensor',
            name='premium_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]