# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-20 05:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preporucivac', '0003_auto_20170820_0306'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interesovanja',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parkovi', models.BigIntegerField()),
                ('spomenici', models.BigIntegerField()),
                ('kafici', models.BigIntegerField()),
                ('muzeji', models.BigIntegerField()),
                ('pozorista', models.BigIntegerField()),
                ('bioskopi', models.BigIntegerField()),
                ('hoteli', models.BigIntegerField()),
                ('tvrdjave', models.BigIntegerField()),
                ('trgovi', models.BigIntegerField()),
                ('verski', models.BigIntegerField()),
                ('ostalo', models.BigIntegerField()),
            ],
        ),
    ]
