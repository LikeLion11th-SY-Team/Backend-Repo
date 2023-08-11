# Generated by Django 4.2.3 on 2023-08-11 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_user_progress'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='progress',
            field=models.IntegerField(choices=[(0, 'Bookmark'), (1, 'Signup'), (2, 'Login'), (3, 'Community'), (4, 'Write'), (5, 'Communicate'), (6, 'Mypage')], default=0),
        ),
    ]