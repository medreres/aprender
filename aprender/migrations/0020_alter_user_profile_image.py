# Generated by Django 4.0.5 on 2022-10-15 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aprender', '0019_alter_user_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(default='icons/user.png', upload_to=''),
        ),
    ]