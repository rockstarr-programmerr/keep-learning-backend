# Generated by Django 3.2.7 on 2021-10-04 15:01

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('classroom', '0003_auto_20211004_2145'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='readingexercise',
            unique_together={('creator', 'identifier')},
        ),
    ]
