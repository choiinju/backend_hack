# Generated by Django 5.0.7 on 2024-07-25 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_user_first_ex'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='card_number',
            field=models.CharField(max_length=20, null=True, unique=True),
        ),
    ]