# Generated by Django 4.1.5 on 2023-07-07 07:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['is_read', '-created']},
        ),
    ]
