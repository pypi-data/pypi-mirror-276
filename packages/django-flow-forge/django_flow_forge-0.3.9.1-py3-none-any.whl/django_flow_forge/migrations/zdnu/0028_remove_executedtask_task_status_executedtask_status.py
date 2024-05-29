# Generated by Django 5.0.2 on 2024-02-25 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_flow_forge', '0027_executedtask_task_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='executedtask',
            name='task_status',
        ),
        migrations.AddField(
            model_name='executedtask',
            name='status',
            field=models.CharField(choices=[('complete', 'Complete'), ('still_running', 'Still Running'), ('failed', 'Failed')], default='still_running', max_length=20),
        ),
    ]
