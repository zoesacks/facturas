# Generated by Django 4.2.5 on 2023-10-02 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturas', '0005_alter_codigofinanciero_codigo'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='estado',
            field=models.CharField(choices=[('enviar', 'Enviar'), ('enviado', 'Enviado')], default='enviar', max_length=20),
        ),
    ]
