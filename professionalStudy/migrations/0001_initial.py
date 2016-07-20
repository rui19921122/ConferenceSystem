# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-18 10:34
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('call_over', '0004_auto_20160718_1034'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfessionalStudy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publish_time', models.DateTimeField(auto_now_add=True)),
                ('title', models.TextField(verbose_name='标题')),
                ('answer', models.TextField(blank=True, verbose_name='答案')),
                ('checked_by_first', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='study_first', to='call_over.CallOverDetail')),
                ('checked_by_forth', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='study_forth', to='call_over.CallOverDetail')),
                ('checked_by_second', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='study_second', to='call_over.CallOverDetail')),
                ('checked_by_third', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='study_third', to='call_over.CallOverDetail')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Department')),
                ('publish_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
