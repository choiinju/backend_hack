# Generated by Django 5.0.7 on 2024-07-27 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0007_alter_user_card_number_alter_user_first_ex'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='point',
            field=models.IntegerField(null=True),
        ),
    ]
