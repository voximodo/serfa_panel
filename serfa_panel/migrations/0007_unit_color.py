# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-04 19:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serfa_panel', '0006_auto_20170404_2122'),
    ]

    operations = [
        migrations.AddField(
            model_name='unit',
            name='color',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
    ]