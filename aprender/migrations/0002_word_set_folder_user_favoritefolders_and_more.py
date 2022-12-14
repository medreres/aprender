# Generated by Django 4.0.5 on 2022-09-22 18:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aprender', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.CharField(max_length=255)),
                ('definition', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Set',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255)),
                ('date', models.DateTimeField()),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('chosenWords', models.ManyToManyField(related_name='chosenWords', to='aprender.word')),
                ('words', models.ManyToManyField(related_name='words', to='aprender.word')),
            ],
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255)),
                ('date', models.DateTimeField()),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('sets', models.ManyToManyField(to='aprender.set')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='favoriteFolders',
            field=models.ManyToManyField(to='aprender.folder'),
        ),
        migrations.AddField(
            model_name='user',
            name='favoriteSets',
            field=models.ManyToManyField(to='aprender.set'),
        ),
    ]
