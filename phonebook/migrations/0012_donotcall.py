# Generated by Django 3.0.8 on 2020-07-12 19:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('phonebook', '0011_auto_20200712_2005'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoNotCall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='phonebook.Lead')),
            ],
        ),
    ]
