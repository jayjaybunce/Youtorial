# Generated by Django 3.0 on 2020-03-23 16:13

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0010_auto_20200321_1515'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stats', models.CharField(choices=[('S', 'Saved'), ('C', 'Completed'), ('G', 'Generated')], default='S', max_length=100)),
                ('saved', models.DateTimeField(default=datetime.datetime(2020, 3, 23, 10, 13, 47, 743089), verbose_name='date saved')),
                ('tutorial', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main_app.Tutorial')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
