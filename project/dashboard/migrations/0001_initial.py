# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-27 18:33
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BuildConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('namespace', models.CharField(max_length=100)),
                ('last_seen', models.DateField(auto_now_add=True)),
                ('build_config', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={})),
            ],
        ),
        migrations.CreateModel(
            name='Environment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('environment', models.CharField(choices=[(b'NP', b'Non-Prod'), (b'PRD', b'Production'), (b'POC', b'POC')], max_length=20, unique=True)),
            ],
            options={
                'ordering': ['environment'],
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=100, unique=True)),
                ('description', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['language'],
            },
        ),
        migrations.AddField(
            model_name='buildconfig',
            name='environment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Environment'),
        ),
        migrations.AddField(
            model_name='buildconfig',
            name='language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.Language'),
        ),
        migrations.AlterUniqueTogether(
            name='buildconfig',
            unique_together=set([('environment', 'namespace', 'name', 'last_seen')]),
        ),
    ]
