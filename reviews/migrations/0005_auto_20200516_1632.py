# Generated by Django 3.0.3 on 2020-05-16 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20200516_1453'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='down_vote',
            new_name='down_votes',
        ),
    ]