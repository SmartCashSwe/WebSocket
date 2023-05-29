# Generated by Django 4.2 on 2023-05-23 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('KasaRegister', '0004_rename_user_kasauser'),
    ]

    operations = [
        migrations.CreateModel(
            name='Licence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('licence', models.CharField(auto_created=True, max_length=12)),
                ('valid_until', models.DateField(auto_now=True)),
                ('kasa', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='KasaRegister.kasauser')),
            ],
        ),
    ]