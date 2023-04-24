# Generated by Django 4.2 on 2023-04-18 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mobile_user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('personal_number', models.CharField(max_length=64)),
                ('password', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Pc_user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pcIdentifier', models.CharField(max_length=64, unique=True)),
                ('mobile_users', models.JSONField()),
            ],
        ),
    ]