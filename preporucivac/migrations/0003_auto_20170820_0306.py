# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-20 01:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('preporucivac', '0002_auto_20170820_2132'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mesto',
            name='x',
        ),
        migrations.RemoveField(
            model_name='mesto',
            name='y',
        ),
    ]