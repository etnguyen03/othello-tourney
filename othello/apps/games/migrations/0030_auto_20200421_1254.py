# Generated by Django 3.0.5 on 2020-04-21 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0029_auto_20200421_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='winner',
            field=models.CharField(choices=[('X', 'Black'), ('O', 'White')], default=None, max_length=1, null=True),
        ),
    ]