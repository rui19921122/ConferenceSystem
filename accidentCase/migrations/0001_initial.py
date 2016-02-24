# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-24 01:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccidentCase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('publish_time', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('publish_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('relative_system', models.ManyToManyField(to='base.ProfessionalSystem')),
            ],
        ),
        migrations.CreateModel(
            name='AccidentClaim',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('claim_time', models.DateTimeField(auto_now_add=True)),
                ('checked_by_first', models.DateTimeField(blank=True)),
                ('checked_by_second', models.DateTimeField(blank=True)),
                ('checked_by_third', models.DateTimeField(blank=True)),
                ('checked_by_forth', models.DateTimeField(blank=True)),
                ('accident', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accidentCase.AccidentCase')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Department')),
            ],
        ),
    ]
