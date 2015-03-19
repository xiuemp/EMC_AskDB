# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category_name', models.CharField(max_length=100)),
                ('type_name', models.CharField(max_length=10)),
                ('time_min', models.IntegerField(default=-1)),
                ('time_max', models.IntegerField(default=-1)),
                ('size_min', models.FloatField(default=-1)),
                ('size_max', models.FloatField(default=-1)),
                ('latency_min', models.FloatField(default=-1)),
                ('latency_max', models.FloatField(default=-1)),
                ('pub_date', models.DateTimeField(verbose_name=b'date published')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_path', models.CharField(max_length=200)),
                ('log_name', models.CharField(max_length=100)),
                ('category_key', models.CharField(max_length=100)),
                ('index_time', models.IntegerField(default=0)),
                ('index_type', models.IntegerField(default=8)),
                ('index_sent', models.IntegerField(default=16)),
                ('index_received', models.IntegerField(default=17)),
                ('index_latency', models.IntegerField(default=18)),
                ('pub_date', models.DateTimeField(verbose_name=b'date published')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='domain',
            name='pd_name',
            field=models.ForeignKey(to='eye.Log'),
            preserve_default=True,
        ),
    ]
