# Generated by Django 4.2.4 on 2023-09-29 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0004_facturacion_num_autorizacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='detallefacturacion',
            name='tipo',
            field=models.CharField(default=1, max_length=2),
            preserve_default=False,
        ),
    ]
