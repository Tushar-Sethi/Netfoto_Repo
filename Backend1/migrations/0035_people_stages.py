# Generated by Django 4.0.2 on 2022-04-01 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend1', '0034_remove_people_stages'),
    ]

    operations = [
        migrations.AddField(
            model_name='people',
            name='stages',
            field=models.TextField(blank=True, default=''),
        ),
    ]
