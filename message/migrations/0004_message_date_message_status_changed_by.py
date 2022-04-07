# Generated by Django 4.0.3 on 2022-04-07 08:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0003_remove_message_status_changed_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 7, 8, 52, 15, 935818)),
        ),
        migrations.AddField(
            model_name='message',
            name='status_changed_by',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]