# Generated by Django 4.0.5 on 2022-10-05 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aprender', '0014_alter_user_recentsets'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='recentSets',
        ),
        migrations.AddField(
            model_name='user',
            name='recentSetsJson',
            field=models.CharField(default='', max_length=64),
        ),
    ]
