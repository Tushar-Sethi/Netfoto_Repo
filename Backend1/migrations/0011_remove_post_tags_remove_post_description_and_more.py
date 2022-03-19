# Generated by Django 4.0.2 on 2022-03-09 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend1', '0010_people_photo_alter_people_birth_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='Tags',
        ),
        migrations.RemoveField(
            model_name='post',
            name='description',
        ),
        migrations.RemoveField(
            model_name='post',
            name='title',
        ),
        migrations.AddField(
            model_name='images',
            name='Tag1',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='images',
            name='Tag2',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='images',
            name='Tag3',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='images',
            name='description',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='images',
            name='title',
            field=models.CharField(default='Default Value', max_length=255),
            preserve_default=False,
        ),
    ]
