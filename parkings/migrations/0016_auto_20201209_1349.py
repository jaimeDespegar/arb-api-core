# Generated by Django 3.1.2 on 2020-12-09 13:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parkings', '0015_notificationegress_photoinbase64'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='estadia',
            unique_together={('userName', 'isActive', 'place')},
        ),
    ]
