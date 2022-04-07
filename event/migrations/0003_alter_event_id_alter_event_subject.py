# Generated by Django 4.0.3 on 2022-04-07 08:47

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_alter_event_board_alter_event_finished_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='id',
            field=models.UUIDField(default=uuid.UUID('61096b30-ea9c-4f4e-bed1-35675e83ab23'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='event',
            name='subject',
            field=models.CharField(choices=[('I need a new feature', 'I need a new feature'), ('I need help', 'I need help'), ('I have remarks about application', 'I have remarks about application'), ('Bug in application', 'Bug in application')], max_length=255),
        ),
    ]