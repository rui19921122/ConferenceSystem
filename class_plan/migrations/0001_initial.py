# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassPlanBase',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('number', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DayDetail',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('department', models.CharField(max_length=100)),
                ('style', models.ForeignKey(to='class_plan.ClassPlanBase')),
            ],
        ),
        migrations.CreateModel(
            name='DayTable',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('publish_time', models.DateTimeField(auto_now_add=True)),
                ('time', models.DateField()),
                ('publish_person', models.ForeignKey(to='base.Person')),
            ],
        ),
        migrations.CreateModel(
            name='SingleClaimDetail',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('content', models.CharField(max_length=500)),
                ('number', models.PositiveSmallIntegerField()),
                ('claim_time', models.DateTimeField(auto_now_add=True)),
                ('department', models.ForeignKey(to='base.Department')),
                ('father_detail', models.ForeignKey(to='class_plan.DayDetail')),
            ],
        ),
        migrations.CreateModel(
            name='SinglePublishDetail',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('content', models.CharField(max_length=500)),
                ('number', models.PositiveSmallIntegerField()),
                ('father_detail', models.ForeignKey(to='class_plan.DayDetail')),
            ],
        ),
        migrations.AddField(
            model_name='daydetail',
            name='table',
            field=models.ForeignKey(to='class_plan.DayTable'),
        ),
    ]
