# Generated by Django 5.1.2 on 2025-01-02 15:38

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('private_messages', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='content',
            field=django_ckeditor_5.fields.CKEditor5Field(),
        ),
    ]
