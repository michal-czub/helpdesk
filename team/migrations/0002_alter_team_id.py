# Generated by Django 4.0.3 on 2022-04-02 20:48

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='id',
            field=models.UUIDField(default=uuid.UUID('46320b95-e011-4fb4-9f04-9c0471b58591'), editable=False, primary_key=True, serialize=False),
        ),
    ]