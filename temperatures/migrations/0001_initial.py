# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Temperature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('temperature', models.FloatField(editable=False)),
                ('correctness', models.BooleanField()),
                ('description', models.CharField(max_length=255)),
                ('measured', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
