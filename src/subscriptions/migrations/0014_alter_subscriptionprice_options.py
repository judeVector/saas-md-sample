# Generated by Django 5.0.6 on 2024-08-06 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0013_subscriptionprice_timestamp_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscriptionprice',
            options={'ordering': ['order', 'featured', '-updated']},
        ),
    ]
