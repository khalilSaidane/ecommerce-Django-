# Generated by Django 3.0.3 on 2020-05-16 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0004_auto_20200516_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentreview',
            name='childs',
            field=models.ManyToManyField(blank=True, null=True, related_name='_commentreview_childs_+', to='comments.CommentReview'),
        ),
    ]
