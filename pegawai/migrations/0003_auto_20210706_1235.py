# Generated by Django 3.1.7 on 2021-07-06 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pegawai', '0002_auto_20210706_1225'),
    ]

    operations = [
        migrations.AddField(
            model_name='pegawaimodel',
            name='jabatan_data',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='pegawaimodel',
            name='jenis_jabatan',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
