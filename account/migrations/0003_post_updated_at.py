# Generated by Django 4.2.7 on 2024-01-11 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]