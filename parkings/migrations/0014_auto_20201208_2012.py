# Generated by Django 3.1.2 on 2020-12-08 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parkings', '0013_auto_20201130_0923'),
    ]

    operations = [
        migrations.AddField(
            model_name='movecamera',
            name='photoInBase64',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='segment',
            name='photoInBase64',
            field=models.TextField(default=''),
        ),
    ]