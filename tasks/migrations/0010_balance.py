# Generated by Django 4.2.4 on 2023-10-09 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0009_miembro'),
    ]

    operations = [
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('gasto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ingreso', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
