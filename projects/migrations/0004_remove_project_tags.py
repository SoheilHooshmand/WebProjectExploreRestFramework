# Generated by Django 4.1.5 on 2023-07-07 19:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_project_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='tags',
        ),
    ]
