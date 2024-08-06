# Generated by Django 5.0.6 on 2024-08-06 16:50

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0012_subscriptionprice_featured_subscriptionprice_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionprice',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscriptionprice',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='subscriptionprice',
            name='featured',
            field=models.BooleanField(default=True, help_text='Featured on Django pricing page.'),
        ),
        migrations.AlterField(
            model_name='subscriptionprice',
            name='order',
            field=models.IntegerField(default=-1, help_text='Ordering on Django pricing page'),
        ),
    ]
