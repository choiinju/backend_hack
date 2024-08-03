# Generated by Django 5.0.7 on 2024-08-02 16:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_alter_user_point'),
    ]

    operations = [
        migrations.CreateModel(
            name='Matched',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('review', models.TextField()),
                ('describe', models.TextField()),
                ('receiving_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_matches', to=settings.AUTH_USER_MODEL)),
                ('yielding_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='yielded_matches', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]