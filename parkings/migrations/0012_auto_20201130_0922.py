# Generated by Django 3.1.2 on 2020-11-30 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parkings', '0011_auto_20201130_0921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuration',
            name='configurationName',
            field=models.CharField(default='config', max_length=200),
        ),
    ]
