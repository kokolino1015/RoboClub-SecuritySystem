# Generated by Django 5.1.2 on 2024-10-20 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_useractivity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='username',
            field=models.CharField(max_length=30),
        ),
    ]
