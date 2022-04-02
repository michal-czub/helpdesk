# Generated by Django 4.0.3 on 2022-04-02 19:57

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.UUIDField(default=uuid.UUID('9949e816-3983-4cc0-8664-b34111c85f6b'), editable=False, primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('is_confirmed', models.BooleanField(default=False)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consultations', to='event.event')),
            ],
        ),
    ]