# Generated by Django 4.2.2 on 2023-08-04 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_total_data_order_vendors'),
        ('foody', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminwallet',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.order'),
        ),
    ]