# Generated by Django 4.0.2 on 2022-03-27 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend1', '0021_post_product_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='people',
            name='step_1',
            field=models.BooleanField(default=False),
        ),
    ]
