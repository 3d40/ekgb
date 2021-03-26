<<<<<<< HEAD
# Generated by Django 3.1.7 on 2021-03-24 02:01
=======
# Generated by Django 3.1 on 2021-03-23 14:45
>>>>>>> 07c1ed949029e742a377262f916420ff6f4997ee

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BerkalaHistoryModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('kgb_nomor', models.CharField(blank=True, max_length=255, null=True)),
                ('kgb_tanggal', models.DateTimeField(auto_now=True, null=True)),
                ('tmt', models.DateField(blank=True, null=True)),
                ('tmt_baru', models.DateField(blank=True, null=True)),
                ('golongan', models.CharField(max_length=5)),
                ('pejabat_ttd', models.CharField(default='GUBERNUR JAMBI', max_length=255)),
                ('mk_lama_tahun', models.IntegerField(blank=True, null=True)),
                ('mk_lama_bulan', models.IntegerField(blank=True, null=True)),
                ('kgb_image', models.FileField(blank=True, null=True, upload_to='media')),
                ('mk_baru_tahun', models.IntegerField(blank=True, null=True)),
                ('mk_baru_bulan', models.IntegerField(blank=True, null=True)),
                ('nilai', models.IntegerField(blank=True, null=True)),
                ('dokumen', models.FileField(blank=True, null=True, upload_to='upload/skberkala/')),
            ],
        ),
        migrations.CreateModel(
            name='DaftarNominatifModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='GolonganModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=50)),
                ('nilai', models.IntegerField()),
                ('simbol', models.CharField(max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='JabatanModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jenis', models.CharField(choices=[('struktural', 'Struktural'), ('jft', 'Fungsional'), ('jfu', 'Fungsional Umum')], default='jfu', max_length=30)),
                ('nama', models.CharField(max_length=100)),
                ('bup', models.IntegerField()),
                ('jenjang', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='OpdModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=255)),
                ('kepala_opd', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PegawaiModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=100)),
                ('nip', models.CharField(max_length=100, null=True)),
                ('pengguna', models.IntegerField(blank=True, null=True)),
                ('alamat', models.CharField(max_length=255)),
                ('telpon', models.CharField(max_length=30)),
                ('gaji_skrg', models.IntegerField(blank=True, default=0, null=True)),
                ('tmt_cpns', models.DateField(blank=True, default=datetime.datetime.now, null=True)),
<<<<<<< HEAD
=======
                ('mk_tahun', models.IntegerField(blank=True, null=True)),
                ('mk_bulan', models.IntegerField(blank=True, null=True)),
>>>>>>> 07c1ed949029e742a377262f916420ff6f4997ee
                ('fhoto', models.ImageField(upload_to='upload/fhoto/')),
                ('golongan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='pegawai.golonganmodel')),
                ('jabatan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='pegawai.jabatanmodel')),
                ('opd', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='pegawai.opdmodel')),
            ],
        ),
        migrations.CreateModel(
            name='ProsesBerkalaModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tanggal', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(blank=True, choices=[('selesai', 'Selesai'), ('tertunda', 'Tertunda'), ('proses', 'Proses')], max_length=20)),
                ('pegawai', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='pegawai.pegawaimodel')),
            ],
        ),
        migrations.CreateModel(
            name='GolonganHistoryModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pengguna', models.IntegerField(blank=True, null=True)),
                ('nip', models.CharField(blank=True, max_length=50, null=True)),
                ('nomor_sk', models.CharField(blank=True, default='S-10225/BKD-2.2/', max_length=150, null=True)),
                ('jenis', models.CharField(blank=True, max_length=50, null=True)),
                ('tanggal', models.DateField(blank=True, default=1998, null=True)),
                ('mk_tahun', models.IntegerField(blank=True, null=True)),
                ('mk_bulan', models.IntegerField(blank=True, null=True)),
                ('dokumen', models.FileField(blank=True, null=True, upload_to='upload/skpangkat/')),
                ('nama', models.ForeignKey(blank=True, default=24, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='pegawai.golonganmodel')),
            ],
            options={
                'managed': (True,),
            },
        ),
        migrations.CreateModel(
            name='GajiModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('masa_kerja', models.IntegerField()),
                ('tbgaji_currency', models.CharField(blank=True, max_length=255, null=True)),
                ('terbilang', models.CharField(blank=True, max_length=255, null=True)),
                ('golongan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='pegawai.golonganmodel')),
            ],
        ),
        migrations.CreateModel(
            name='AkunModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pegawai', models.CharField(blank=True, max_length=50, null=True)),
                ('jenis_akun', models.CharField(choices=[('pegawai', 'Pegawai'), ('operatoropd', 'OperatorOpd'), ('operator', 'Operator'), ('admin', 'Administrator')], max_length=20)),
                ('akun', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('opd_akses', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='pegawai.opdmodel')),
            ],
        ),
    ]
