# Generated by Django 3.0.8 on 2020-07-12 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phonebook', '0002_auto_20200712_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='phonebook',
            name='csv_file',
            field=models.FilePathField(default=None, path='static/phonebooks'),
        ),
        migrations.AlterField(
            model_name='phonebook',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
