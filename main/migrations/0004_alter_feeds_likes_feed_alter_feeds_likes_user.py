# Generated by Django 4.2.16 on 2024-10-18 08:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0003_follower_friendship'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feeds_likes',
            name='feed',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='feed_likes', to='main.feeds'),
        ),
        migrations.AlterField(
            model_name='feeds_likes',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
