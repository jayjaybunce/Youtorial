# Generated by Django 3.0.4 on 2020-03-21 08:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_status_stats'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='saved',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 21, 2, 25, 9, 57885), verbose_name='date saved'),
        ),
        migrations.AlterField(
            model_name='status',
            name='stats',
            field=models.CharField(choices=[('S', 'Saved'), ('C', 'Completed'), ('G', 'Generated')], default='S', max_length=100),
        ),
    ]