# Generated by Django 4.2.21 on 2025-05-13 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='sesion_key',
            new_name='session_key',
        ),
    ]
