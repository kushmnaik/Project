# Generated by Django 3.2.8 on 2021-11-13 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0011_delivery_restaurant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='restaurant',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='restaurant.restaurant'),
        ),
    ]
