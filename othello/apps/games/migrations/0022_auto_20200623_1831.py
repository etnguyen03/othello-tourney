# Generated by Django 3.0.7 on 2020-06-23 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0021_submission_is_legacy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameerror',
            name='error_code',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='gameerror',
            name='error_msg',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='gamelog',
            name='message',
            field=models.TextField(default=''),
        ),
    ]