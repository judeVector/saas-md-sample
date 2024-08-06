# Generated by Django 5.0.6 on 2024-07-26 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('subscriptions', '0004_subscription_permisssion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='permisssion',
            field=models.ManyToManyField(limit_choices_to={'codename__in': ['advanced', 'pro', 'basic', 'basic_ai'], 'content_type__app_label': 'subscriptions'}, to='auth.permission'),
        ),
    ]
