# Generated by Django 4.0.3 on 2022-04-03 18:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='id',
            field=models.UUIDField(default=uuid.UUID('ca2e6cf1-a8ba-46bc-98ba-b0268507f032'), editable=False, primary_key=True, serialize=False),
        ),
    ]
