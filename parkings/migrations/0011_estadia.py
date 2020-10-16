# Generated by Django 3.1.2 on 2020-10-16 22:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parkings', '0010_notification_place'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estadia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrival', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parkings.segment')),
                ('placeUsed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parkings.place')),
            ],
        ),
    ]
