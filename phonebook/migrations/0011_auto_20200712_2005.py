# Generated by Django 3.0.8 on 2020-07-12 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phonebook', '0010_auto_20200712_1957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selection',
            name='description',
            field=models.CharField(max_length=30),
        ),
    ]