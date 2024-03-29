# Generated by Django 4.2.8 on 2024-01-04 08:37

import KasaRegister.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KasaRegister', '0002_alter_kasauser_revisorer'),
    ]

    operations = [
        migrations.AddField(
            model_name='kasauser',
            name='download',
            field=models.FileField(blank=True, null=True, upload_to=KasaRegister.models.get_download_path),
        ),
        migrations.AlterField(
            model_name='kasauser',
            name='kassa_list',
            field=models.JSONField(default={'LäggTillArtikel': [], 'LäggTillHuvudgrupp': [], 'UppdateraArtikel': [], 'UppdateraBokforing': [], 'UppdateraHuvudgrupp': []}),
        ),
    ]
