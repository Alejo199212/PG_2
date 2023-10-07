# Generated by Django 4.2.4 on 2023-09-20 03:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('evento', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='facturacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_factura', models.CharField(max_length=100)),
                ('serie_factura', models.CharField(max_length=100)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('id_evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evento.evento')),
            ],
        ),
    ]