# Generated by Django 5.0 on 2023-12-12 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('at_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atcharacter',
            name='description',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='atcharacter',
            name='friends',
            field=models.JSONField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='atcharacter',
            name='real_name',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='atcharacter',
            name='short_description',
            field=models.CharField(max_length=500, null=True),
        ),
    ]