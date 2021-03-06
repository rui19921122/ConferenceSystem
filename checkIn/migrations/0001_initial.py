# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-20 14:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
        ('worker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckIn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('class_number', models.CharField(choices=[('1', '第一班'), ('2', '第二班')], max_length=1)),
                ('confirm_people', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Person')),
                ('json', models.ManyToManyField(to='worker.Worker')),
            ],
        ),
    ]
