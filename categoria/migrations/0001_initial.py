# Generated by Django 4.2.4 on 2023-08-30 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categorias',
            fields=[
                ('id_categoria', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_categoria', models.CharField(max_length=250)),
                ('descripcion_categoria', models.CharField(max_length=300)),
            ],
        ),
    ]