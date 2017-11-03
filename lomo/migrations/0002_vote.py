# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-16 06:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lomo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='频道名')),
                ('header', models.CharField(blank=True, max_length=200, null=True, verbose_name='标题')),
                ('subheader', models.CharField(blank=True, max_length=200, null=True, verbose_name='副标题')),
                ('header_image', models.ImageField(blank=True, null=True, upload_to='header_image', verbose_name='图片')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]