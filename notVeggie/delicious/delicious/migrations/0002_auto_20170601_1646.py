# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-01 15:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('delicious', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='nome_cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]