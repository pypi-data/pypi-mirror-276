# Generated by Django 5.0.2 on 2024-02-15 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_flow_forge', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='processtask',
            name='task_output',
            field=models.JSONField(default=dict),
        ),
    ]
