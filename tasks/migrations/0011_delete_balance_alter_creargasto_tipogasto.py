# Generated by Django 4.2.4 on 2023-10-15 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0010_balance'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Balance',
        ),
        migrations.AlterField(
            model_name='creargasto',
            name='TipoGasto',
            field=models.CharField(choices=[('servicios', 'Servicio'), ('deuda', 'Deuda'), ('comida', 'Comida'), ('hogar', 'Hogar'), ('educacion', 'Educacion'), ('ocio', 'Ocio'), ('otros', 'Otros')], max_length=50),
        ),
    ]