# Generated by Django 3.0 on 2020-03-21 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_auto_20200320_0120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorial',
            name='rating',
            field=models.IntegerField(null=True),
        ),
    ]
