# Generated by Django 4.1.4 on 2022-12-25 00:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0002_websiteuser_alter_salead_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='salead',
            old_name='user',
            new_name='author',
        ),
    ]