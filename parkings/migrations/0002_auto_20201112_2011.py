# Generated by Django 3.1.2 on 2020-11-12 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parkings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bikeowner',
            name='movie',
            field=models.CharField(default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='bikeowner',
            name='pet',
            field=models.CharField(default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='bikeowner',
            name='street',
            field=models.CharField(default=None, max_length=200, null=True),
        ),
    ]