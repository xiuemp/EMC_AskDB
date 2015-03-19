# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eye', '0002_domain_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='domain',
            name='domain_name',
            field=models.CharField(default=b'null', max_length=100),
            preserve_default=True,
        ),
    ]
