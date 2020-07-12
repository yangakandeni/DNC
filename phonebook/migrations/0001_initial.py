# Generated by Django 3.0.8 on 2020-07-12 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_name', models.CharField(max_length=30)),
                ('contact_number', models.CharField(max_length=30)),
                ('age', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Selection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=2)),
                ('description', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Phonebook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('date', models.DateField()),
                ('leads', models.ManyToManyField(to='phonebook.Lead')),
            ],
        ),
        migrations.CreateModel(
            name='CallDetailRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='phonebook.Lead')),
                ('selection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='phonebook.Selection')),
            ],
        ),
    ]