# Generated by Django 4.2.1 on 2023-05-28 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='is_vendor',
            field=models.BooleanField(default=False),
        ),
    ]