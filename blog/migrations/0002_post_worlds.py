# Generated by Django 2.2.25 on 2022-01-07 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='worlds',
            field=models.TextField(default=''),
        ),
    ]