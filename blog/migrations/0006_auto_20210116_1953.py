# Generated by Django 3.1.4 on 2021-01-16 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20210114_1828'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created']},
        ),
        migrations.AddField(
            model_name='post',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.TextField(blank=True),
        ),
    ]