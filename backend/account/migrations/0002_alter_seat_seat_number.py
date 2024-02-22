# Generated by Django 5.0.1 on 2024-02-14 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seat',
            name='seat_number',
            field=models.PositiveIntegerField(default=0, help_text='Seat number for identity', verbose_name='Seat Number'),
        ),
    ]