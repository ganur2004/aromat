# Generated by Django 4.2.13 on 2024-06-07 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0017_alter_aromat_code_alter_aromat_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aromat',
            name='code',
            field=models.CharField(max_length=5, verbose_name='Код'),
        ),
    ]
