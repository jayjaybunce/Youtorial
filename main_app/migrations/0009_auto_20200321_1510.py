# Generated by Django 3.0 on 2020-03-21 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_auto_20200321_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorial',
            name='video_url',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
