# Generated by Django 5.0.7 on 2024-07-25 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='first_ex',
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
    ]
