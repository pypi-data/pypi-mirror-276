# Generated by Django 5.0.2 on 2024-02-19 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_flow_forge', '0019_executedprocess_process_id_snapshot_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='executedtask',
            name='task_name_snapshot',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
