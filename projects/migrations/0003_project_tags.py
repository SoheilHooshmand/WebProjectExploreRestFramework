# Generated by Django 4.1.5 on 2023-07-07 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_remove_project_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='projects.tag'),
        ),
    ]