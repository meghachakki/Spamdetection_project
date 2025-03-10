# Generated by Django 4.1.2 on 2024-06-24 04:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0007_profile_blocked_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='blocked_users',
        ),
        migrations.AddField(
            model_name='profile',
            name='contacts',
            field=models.ManyToManyField(blank=True, related_name='contacts', to=settings.AUTH_USER_MODEL),
        ),
    ]
