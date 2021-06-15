from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

# Create your models here.
class PegawaiModel(models.Model):
    nama = models.CharField(max_length=100)
    jabatan = models.ForeignKey('JabatanModel', models.DO_NOTHING, blank=True, null=True)
    nip = models.CharField(max_length=100, null=True)
    opd = models.ForeignKey('OpdModel', models.DO_NOTHING, blank=True, null=True)
    golongan = models.ForeignKey('GolonganModel', models.DO_NOTHING, null=True, blank=True)
    pengguna = models.IntegerField(blank=True, null=True)
    alamat  = models.CharField(max_length=255)
    telpon  = models.CharField(max_length=30)
    gaji_skrg = models.IntegerField(blank=True, null=True, default=0)
    tmt_cpns = models.DateField(default=datetime.datetime.now, null=True, blank=True)
    fhoto = models.ImageField(upload_to ='upload/fhoto/')
    nominasi = models.BooleanField(default=False)
    

    def __str__(self):
        return self.nama

class GolonganModel(models.Model):
    nama = models.CharField(max_length=50)
    nilai = models.IntegerField()
    simbol =models.CharField(max_length=10, null=True)
    grade =models.IntegerField(default=0,blank=True, null=True)

    def __str__(self):
        return self.nama

class GolonganHistoryModel(models.Model):
    pengguna = models.IntegerField(null=True, blank=True)
    nip = models.CharField(max_length=50, null=True, blank=True, verbose_name= 'NIP')
    nama = models.ForeignKey(GolonganModel ,models.DO_NOTHING, null=True,blank=True,default=24, verbose_name='Nama Golongan')
    nomor_sk = models.CharField(max_length=150, null=True,blank=True, default="S-10225/BKD-2.2/", verbose_name="Nomor SK")
    jenis = models.CharField(max_length=50, null=True, blank=True)
    tanggal = models.DateField(default=2021-3-20, blank=True, null=True, verbose_name="Tanggal")
    dokumen = models.FileField(upload_to='upload/skpangkat/', blank=True, null=True, verbose_name="Dokumen")
    mk_tahun = models.IntegerField(null=True, default=0)
    mk_bulan = models.IntegerField(null=True, default=0)
    
    class Meta:
        managed=True,
    
    def __str__(self):
        return self.nip
        

class OpdModel(models.Model):
    nama = models.CharField(max_length=255)
    kepala_opd = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.nama

class JabatanModel(models.Model):
    pilihan_jenis = [
        ('struktural', 'Struktural'),
        ('jfu','Fungsional Umum'),
        ('jft1', 'Ahli Pertma'),
        ('jft2', 'Ahli Muda'),
        ('jft3', 'Ahli Madya'),
        ('jft4', 'Ahli Utama'),
        ('jft5', 'Pelaksana Pemula'),
        ('jft6', 'Pelaksana'),
        ('jft7', 'Ahli Utama'),


    ]
    jenis = models.CharField(max_length=30, choices=pilihan_jenis, default='jfu')
    nama = models.CharField(max_length=100)
    bup = models.IntegerField()
    jenjang = models.CharField(max_length=15)

    def __str__(self):
        return self.nama

class GajiModel(models.Model):
    masa_kerja = models.IntegerField()
    golongan = models.ForeignKey('GolonganModel', models.DO_NOTHING, blank=True, null=True)
    tbgaji_currency = models.CharField(blank=True, null=True, max_length=255)
    terbilang = models.CharField(blank=True, null=True, max_length=255)

    def __str__(self):
        return self.golongan

class BerkalaHistoryModel(models.Model):
    username    = models.CharField(max_length=255, blank=True, null=True)
    kgb_nomor = models.CharField(max_length=255, blank=True, null=True)
    kgb_tanggal = models.DateTimeField(auto_now=True, blank=True, null=True)
    tmt         = models.DateField(blank=True, null=True)
    tmt_baru    = models.DateField(blank=True, null=True)
    golongan    = models.CharField(max_length=5)
    pejabat_ttd = models.CharField(max_length=255, default='GUBERNUR JAMBI')
    mk_lama_tahun  = models.IntegerField(blank=True, null=True)
    mk_lama_bulan  = models.IntegerField(blank=True, null=True)
    kgb_image = models.FileField(blank=True, null=True, upload_to = 'media')
    mk_baru_tahun  = models.IntegerField(blank=True, null=True)
    mk_baru_bulan  = models.IntegerField(blank=True, null=True)
    nilai= models.IntegerField(null=True, blank=True)
    dokumen = models.FileField(upload_to='upload/skberkala/', blank=True, null=True)
    
    
    def __str__(self):
        return self.golongan
    

class AkunModel(models.Model):
    JENIS_AKUN_CHOICES = (
        ('pegawai','Pegawai'),
        ('operatoropd', 'OperatorOpd'),
        ('operator', 'Operator'),
        ('admin', 'Administrator'),

    )
    akun = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    pegawai = models.CharField(max_length=50, blank=True, null=True)
    jenis_akun = models.CharField(max_length=20, choices=JENIS_AKUN_CHOICES)
    opd_akses = models.ForeignKey('OpdModel', models.DO_NOTHING, blank=True, null=True)

    def __unicode__(self):
        return self.akun


class ProsesBerkalaModel(models.Model):
    STATUS_CHOICES = (
        ('selesai','Selesai'),
        ('tertunda', 'Tertunda'),
        ('proses', 'Proses'),
    )
    gaji = models.ForeignKey('GajiModel', models.DO_NOTHING, blank=True, null=True)
    jabatan = models.ForeignKey('JabatanModel', models.DO_NOTHING, blank=True, null=True)
    mk_tahun = models.IntegerField(blank=True, null=True)
    mk_bulan = models.IntegerField(blank=True, null=True)
    pegawai = models.ForeignKey('PegawaiModel', models.DO_NOTHING, blank=True, null=True)
    tanggal = models.DateTimeField(auto_now_add=timezone.now, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True)

    def __str__(self):
        return self.pegawai

class NominatifxModels(models.Model):
    bahanchoice = (
        ('l','Lengkap'),
        ('tl', 'Tidak Lengkap'),
    )
    golongan = models.ForeignKey('GolonganModel', models.DO_NOTHING, null=True, blank=True)
    gaji = models.ForeignKey('GajiModel', models.DO_NOTHING, blank=True, null=True)
    jabatan = models.ForeignKey('JabatanModel', models.DO_NOTHING, blank=True, null=True)
    mk_tahun = models.IntegerField(blank=True, null=True)
    mk_bulan = models.IntegerField(blank=True, null=True)
    mkb_tahun = models.IntegerField(blank=True, null=True)
    mkb_bulan = models.IntegerField(blank=True, null=True)
    pegawai = models.ForeignKey('PegawaiModel', models.DO_NOTHING, blank=True)
    tanggal = models.DateTimeField(auto_now_add=timezone.now, blank=True)
    tmt_kgb = models.DateField(blank=True, null=True)
    bahan = models.CharField(max_length=20, choices=bahanchoice, blank=True)
    
    def __str__(self):
        return self.pegawai


