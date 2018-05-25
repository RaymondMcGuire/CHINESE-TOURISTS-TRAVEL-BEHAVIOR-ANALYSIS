# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-07 01:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('articleName', models.CharField(max_length=100)),
                ('authorPos', models.CharField(max_length=20)),
                ('authorSex', models.CharField(max_length=20)),
                ('startTime', models.CharField(max_length=50)),
                ('people', models.CharField(max_length=50)),
                ('duringDay', models.CharField(max_length=50)),
                ('cost', models.CharField(max_length=20)),
                ('articleInfo', models.TextField()),
                ('keyWords', models.TextField()),
            ],
        ),
    ]