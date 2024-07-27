# Generated by Django 5.0.7 on 2024-07-27 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0004_alter_user_first_ex'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='login_id',
            field=models.CharField(max_length=30, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
