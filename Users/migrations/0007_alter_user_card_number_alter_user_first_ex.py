# Generated by Django 5.0.7 on 2024-07-27 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0006_remove_user_login_id_alter_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='card_number',
            field=models.CharField(max_length=16, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_ex',
            field=models.CharField(max_length=100, null=True),
        ),
    ]