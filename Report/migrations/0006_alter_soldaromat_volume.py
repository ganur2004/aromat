# Generated by Django 4.2.13 on 2024-06-03 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0005_soldaromat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soldaromat',
            name='volume',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='Объем'),
        ),
    ]
