# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-19 01:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lomo', '0004_auto_20171018_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='thumb_img',
            field=models.ImageField(blank=True, null=True, upload_to='thumb_img', verbose_name='缩略图'),
        ),
    ]