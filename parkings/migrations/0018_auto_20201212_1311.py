# Generated by Django 3.0.5 on 2020-12-12 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parkings', '0017_auto_20201209_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estadia',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]