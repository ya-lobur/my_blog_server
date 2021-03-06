# Generated by Django 3.1.4 on 2021-02-28 08:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0005_auto_20210218_0917'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_verified',
            field=models.BooleanField(default=False, verbose_name='verified'),
        ),
        migrations.AddField(
            model_name='profile',
            name='verification_uuid',
            field=models.UUIDField(default=uuid.uuid4, verbose_name='Unique Verification UUID'),
        ),
    ]
