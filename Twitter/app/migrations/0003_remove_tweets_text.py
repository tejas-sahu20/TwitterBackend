# Generated by Django 5.0.6 on 2024-06-29 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_users_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweets',
            name='text',
        ),
    ]
