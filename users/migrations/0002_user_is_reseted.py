# Generated by Django 4.2.4 on 2023-08-15 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_reseted',
            field=models.BooleanField(default=False, verbose_name='비밀번호 초기화됨'),
        ),
    ]
