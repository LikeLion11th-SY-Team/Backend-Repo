# Generated by Django 4.2.3 on 2023-08-08 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_social',
            field=models.BooleanField(default=False, verbose_name='소셜로그인 유저'),
        ),
    ]
