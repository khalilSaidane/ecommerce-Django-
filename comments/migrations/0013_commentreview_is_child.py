# Generated by Django 3.0.3 on 2020-05-17 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0012_auto_20200517_0016'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentreview',
            name='is_child',
            field=models.BooleanField(default=False),
        ),
    ]
