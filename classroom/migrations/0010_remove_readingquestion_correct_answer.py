# Generated by Django 3.2.7 on 2021-10-05 16:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0009_auto_20211005_2232'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='readingquestion',
            name='correct_answer',
        ),
    ]
