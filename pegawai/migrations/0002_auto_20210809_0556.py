# Generated by Django 3.1.7 on 2021-08-09 05:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pegawai', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opdmodel',
            name='kepala_opd',
            field=models.ForeignKey(blank=True, default=88761, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='pegawai.pegawaimodel'),
        ),
    ]
