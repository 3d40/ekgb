# Generated by Django 3.1.7 on 2021-08-16 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pegawai', '0003_auto_20210812_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='berkalahistorymodel',
            name='dokumen',
            field=models.FileField(blank=True, null=True, upload_to='skberkala/'),
        ),
        migrations.AlterField(
            model_name='golonganhistorymodel',
            name='gambar',
            field=models.FileField(blank=True, null=True, upload_to='berkas/'),
        ),
    ]
