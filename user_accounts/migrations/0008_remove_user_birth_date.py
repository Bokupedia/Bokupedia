# Generated by Django 5.1.4 on 2025-01-12 11:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_accounts', '0007_remove_user_comment_count_remove_user_like_count_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='birth_date',
        ),
    ]
