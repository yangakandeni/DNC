# Generated by Django 3.0.8 on 2020-07-12 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('phonebook', '0006_auto_20200712_1631'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lead',
            name='phonebook',
        ),
        migrations.AddField(
            model_name='lead',
            name='phonebook',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='leads', to='phonebook.Phonebook'),
            preserve_default=False,
        ),
    ]