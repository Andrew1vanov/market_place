# Generated by Django 5.0.2 on 2024-02-12 15:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='abailable',
            new_name='available',
        ),
    ]