# Generated by Django 4.2.3 on 2023-08-13 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_progress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
