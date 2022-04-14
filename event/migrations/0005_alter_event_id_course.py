# Generated by Django 4.0.3 on 2022-04-12 13:05

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_alter_event_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='id',
            field=models.UUIDField(default=uuid.UUID('7260e4a7-b836-4a14-9815-08bf81c4b8ae'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('attachment', models.FileField(blank=True, upload_to='')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='event.event')),
            ],
        ),
    ]