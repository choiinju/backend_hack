# Generated by Django 5.0.7 on 2024-07-27 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0008_user_point'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
