# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfessionalStudy',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('publish_time', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('checked_by_first', models.DateTimeField(blank=True)),
                ('checked_by_second', models.DateTimeField(blank=True)),
                ('checked_by_third', models.DateTimeField(blank=True)),
                ('checked_by_forth', models.DateTimeField(blank=True)),
                ('department', models.ForeignKey(to='base.Department')),
                ('publish_person', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
