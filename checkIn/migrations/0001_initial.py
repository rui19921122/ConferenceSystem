# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckIn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('class_number', models.CharField(max_length=1, choices=[('1', '第一班'), ('2', '第二班')])),
                ('confirm_people', models.ForeignKey(to='base.Person')),
            ],
        ),
    ]
