# Generated by Django 3.2.7 on 2021-10-05 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0006_readingquestion_passage'),
    ]

    operations = [
        migrations.AddField(
            model_name='readingquestion',
            name='answers',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.DeleteModel(
            name='ReadingAnswer',
        ),
    ]
