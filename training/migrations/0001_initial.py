# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-24 21:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('held_on', models.DateField()),
                ('details_url', models.URLField(blank=True)),
                ('attendees', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]