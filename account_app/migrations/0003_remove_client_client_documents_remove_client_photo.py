# Generated by Django 5.1.3 on 2024-11-30 23:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account_app', '0002_bank_phonenumber_client_phonenumber_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='client_documents',
        ),
        migrations.RemoveField(
            model_name='client',
            name='photo',
        ),
    ]
