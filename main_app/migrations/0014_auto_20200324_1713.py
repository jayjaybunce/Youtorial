# Generated by Django 3.0 on 2020-03-24 23:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0013_merge_20200324_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='photo_url',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='status',
            name='saved',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 24, 17, 13, 28, 194270), verbose_name='date saved'),
        ),
    ]
