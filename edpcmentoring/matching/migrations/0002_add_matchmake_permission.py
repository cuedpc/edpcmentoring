# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-29 18:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matching', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invitation',
            options={'permissions': (('matchmake', 'Can matchmake mentors and mentees'),)},
        ),
    ]
