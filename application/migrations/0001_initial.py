# Generated by Django 4.0.3 on 2022-04-02 19:57

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.UUIDField(default=uuid.UUID('5ac0548e-9b1d-4858-a892-3897bc8f0d88'), editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='project.project')),
            ],
        ),
    ]
