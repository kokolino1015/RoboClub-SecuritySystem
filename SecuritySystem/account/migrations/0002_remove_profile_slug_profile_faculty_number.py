# Generated by Django 5.1.2 on 2024-10-18 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='slug',
        ),
        migrations.AddField(
            model_name='profile',
            name='faculty_number',
            field=models.CharField(default=12, max_length=9),
            preserve_default=False,
        ),
    ]