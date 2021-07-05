from django.db.models import query
from django.db.models.expressions import Value, ValueRange
from django.db.models.query import QuerySet, ValuesListIterable
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from .forms import UserLoginForm
from django.contrib.auth import (
    authenticate,
    login,
    logout)
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
import csv
import io
from .models import *
import urllib
import json
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView
from . forms import *
import datetime
from dateutil.relativedelta import *
from django.core.exceptions import MultipleObjectsReturned
from itertools import count, zip_longest
from django.http import Http404
from django.views.generic import ListView, DetailView, View
from django.views.generic.detail import SingleObjectMixin
from .filter import FilterPegawai
import os.path
from xhtml2pdf import pisa
from django.template.loader import get_template
# Create your views here.

urlpegawai = 'http://202.179.184.151:8000/nip/?search='
urlcompany = 'http://202.179.184.151:8000/nip/?company='
urlpangkat = 'http://202.179.184.151:8000/riwayatpangkat/?search='


def LoginView(request):
    if request.POST:
        user = authenticate(
            username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            akun = AkunModel.objects.get(akun_id=user.id)
            request.session['opd_akses'] = akun.opd_akses.id
            if user.is_active:
                try:
                    request.session['username'] = request.POST['username']
                    login(request, user)
                    return redirect('pegawai:index')
                except:
                    messages.add_m/ge(request, messages.INFO,
                                     'User belum terverifikasi')
        else:
            messages.add_message(request, messages.INFO,
                                 'Username atau password Anda salah')
    return render(request, 'registration/login.html')


def LogoutView(request):
    try:
        logout(request)
        del request.session['username']
    except KeyError:
        pass
    return render(request, 'registration/login.html')


@login_required()
def IndexView(request):
    request.session['username']
    opdakses = request.session['opd_akses']
    pegawai = PegawaiModel.objects.filter(opd_id=opdakses)
    usulan = len(NominatifxModels.objects.filter(opd=opdakses))
    proses = len(ProsesBerkalaModel.objects.filter(opd=opdakses))
    selesai = len(NominatifSelesaiModels.objects.filter(opd=opdakses))
    jumlah = len(pegawai)
    # cari TMT_CPNS
    for x in pegawai:
        tahun = int(x.nip[8:12])
        bulan = int(x.nip[12:14])
        tanggal = 1
        cpns = datetime.date(tahun, bulan, tanggal)
        q = get_object_or_404(PegawaiModel, id=x.id)
        q.tmt_cpns = cpns
        q.save()
    return render(request, 'pegawai/dahsboard.html', {'pegawai': pegawai, 'jumlah': jumlah, 'usulan': usulan, 'selesai': selesai, 'proses':proses})


@login_required()
def HitungPangkatView(request, id):
    template_name = 'pegawai/detail.html'
    request.session['username']
    opdakses = request.session['opd_akses']
    pegawai = get_object_or_404(PegawaiModel, id=id)
    print(pegawai.id)
    pangkat = urllib.request.urlopen(urlpangkat + str(pegawai.id))
    json_pangkat = json.load(pangkat)
    context = {
        'pegawai':pegawai
        }
    for pkt in json_pangkat:
        list_pangkat = GolonganHistoryModel.objects.filter(pengguna=pegawai.id).update_or_create(
            id=pkt['id'], 
            pengguna=pkt['partner'], 
            nama_id=pkt['golongan_id_history'], 
            nip=pegawai.nip, jenis=pkt['jenis'], 
            tanggal=pkt['date'])
    return render(request, template_name,context)


def RiwayatPangkatView(request, nip):
    request.session['username']
    opdakses = request.session['opd_akses']
    pangkat = GolonganHistoryModel.objects.filter(nip=nip).order_by('-tanggal')
    pegawai = get_object_or_404(PegawaiModel, nip=nip)
    return render(request, 'pegawai/riwayatpangkat.html', {'object_list': pangkat, 'pegawai': pegawai})


class Pegawai(ListView):
    model = PegawaiModel
    ordering = ['tmt_cpns']
    template_name = 'pegawai/pegawaimodel_list.html'
    paginate_by = 25

    def get_queryset(self):
        self.request.session['username']
        opdakses = self.request.session['opd_akses']
        self.queryset = self.model.objects.filter(opd_id=opdakses)
        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, PegawaiModel):
                queryset = self.queryset.all()

        # elif self.model is not None:
        #     queryset = self.model._default_manager.all()
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {
                    'cls': self.__class__.__name__
                }
            )
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset


def CariView(request):
    request.session['username']
    opdakses = request.session['opd_akses']
    queryset = PegawaiModel.objects.filter(opd_id=opdakses)
    cari = request.GET.get('search', '')
    if cari is not None and cari != '':
        caripegawai = PegawaiModel.objects.filter(
            opd_id=opdakses, nama__icontains=cari)
    else:
        return redirect('pegawai:pegawai')
    return render(request, 'pegawai/caripegawai_list.html', {'object_list': caripegawai})


def NominatifViews(request):
    tmtkgb_post = request.POST.get('tmtkgb', {})
    request.session['tmtkgb'] = tmtkgb_post
    request.session['username']
    opdakses = request.session['opd_akses']
    pangkat = GolonganHistoryModel.objects.filter(jenis='cpns')
    # cari TMT_CPNS\
    if request.method == 'POST':
        pegawai = PegawaiModel.objects.filter(opd_id=opdakses)
        jumlah = len(pegawai)
        for x in pegawai:
            tahun = int(x.nip[8:12])
            bulan = int(x.nip[12:14])
            tanggal = 1
            cpns = datetime.date(tahun, bulan, tanggal)
            tmtkgb_date = datetime.datetime.strptime(
                tmtkgb_post, '%Y-%m-%d').date()
            nominasi = relativedelta(tmtkgb_date, cpns).years % 2 == 0 and relativedelta(tmtkgb_date, cpns).months == 0
            nom = pegawai.get(id=x.id)
            nom.nominasi = nominasi
            nom.tmt_cpns = cpns
            nom.save()
            data = pegawai.filter(nominasi=True)
        return render(request, 'pegawai/daftarnominatif.html', {'data': data, 'tmtkgb_date': tmtkgb_date})
    return render(request, 'pegawai/daftarnominatif.html')


class NominatifList(ListView):
    model = NominatifxModels
    ordering = ['tmt_kgb']
    template_name = "nominatiflist.html"

    def get_queryset(self):
        self.request.session['username']
        opdakses = self.request.session['opd_akses']
        queryset = self.model.objects.filter(opd=opdakses)
        for data in queryset:
            print(data.pegawai)
        return queryset


def NominatifDetailView(request, id):
    request.session['username']
    opdakses = request.session['opd_akses']
    data = get_object_or_404(PegawaiModel, id=id)
    gol = get_object_or_404(GolonganModel, id =data.golongan_id)
    print(data.nama, data.golongan_id)
    pangkat = get_object_or_404(GolonganHistoryModel, pengguna=data.id, nama=data.golongan)
    nominatif = get_object_or_404(NominatifxModels, pegawai_id=data.id)
    gaji = get_object_or_404(GajiModel, id=nominatif.gaji_id)
    return render(request, "pegawai/detailnominatif.html", {'pangkat': pangkat,  'data': data, 'nom': nominatif, 'gaji': gaji})


def CetakPdfFile(request, id):
    request.session['username']
    opdakses = request.session['opd_akses']
    template_path = 'pegawai/cetakpdf.html'
    pegawai = get_object_or_404(PegawaiModel, id=id)
    pangkat = get_object_or_404(GolonganHistoryModel, nama_id=pegawai.golongan, pengguna=pegawai.id)
    simbol = get_object_or_404(GolonganModel, id=pegawai.golongan_id)
    nominatif = get_object_or_404(ProsesBerkalaModel, pegawai_id=pegawai.id)
    gajibaru = get_object_or_404(GajiModel, golongan_id=pegawai.golongan, masa_kerja=nominatif.mkb_tahun)
    gajilama = get_object_or_404(GajiModel, golongan_id=pegawai.golongan, masa_kerja=nominatif.mk_tahun)
    opd = get_object_or_404(OpdModel, id=pegawai.opd_id)
    kgbnext = nominatif.tmt_kgb+relativedelta(years=+2)
    inputselesai = NominatifSelesaiModels.objects.get_or_create(
        golongan_id=nominatif.golongan_id,
        gaji_id=nominatif.gaji_id,
        jabatan=nominatif.jabatan,
        mk_tahun=nominatif.mk_tahun,
        mk_bulan=nominatif.mk_bulan,
        mkb_tahun=nominatif.mkb_tahun,
        mkb_bulan=nominatif.mkb_bulan,
        pegawai_id=nominatif.pegawai_id,
        opd_id=nominatif.opd_id,
        tmt_kgb=nominatif.tmt_kgb,
    )
    inputhistory = GolonganHistoryModel.objects.get_or_create(
        pengguna = pegawai.id,
        nip = pegawai.nip,
        nama_id = pegawai.golongan_id,
        jenis = "sk_kgb",
        tanggal = nominatif.tmt_kgb,
        mk_tahun = nominatif.mkb_tahun,
        mk_bulan = nominatif.mkb_bulan,
        tglpenetapan = nominatif.tanggal
    )
    nominatif.delete()
    # kepelaopd = get_object_or_404(PegawaiModel, id=opd.kepala_opd)
    context = {
        'nominatif': nominatif, 
        'data': pegawai, 
        'pangkat': pangkat,
        'gajibaru': gajibaru, 
        'gajilama': gajilama, 
        'kgbnext': kgbnext, 
        'simbol': simbol}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def Hitungmasakerja(request, id):
    request.session['username']
    opdakses = request.session['opd_akses']
    pangkat = get_object_or_404(GolonganHistoryModel, id=id)
    data = get_object_or_404(PegawaiModel, nip=pangkat.nip)
    golonganall = GolonganHistoryModel.objects.filter(pengguna=data.id).order_by('-tanggal')
    cpnscek = get_object_or_404(GolonganHistoryModel, pengguna=data.id, jenis="cpns")
    pnscek = get_object_or_404(GolonganHistoryModel, pengguna=data.id, jenis="pns")
    pangkatgolongan = get_object_or_404(GolonganHistoryModel, pengguna=data.id, id=id)
    golongandasarfilter = GolonganHistoryModel.objects.filter(pengguna=data.id, jenis="pangkat_golongan")
    for i in golonganall:
        # golongan2
        if cpnscek.nama_id == 19 or cpnscek.nama_id == 20 or cpnscek.nama_id == 21:
            cpnscek.mk_tahun = 3
            cpnscek.mk_bulan = 0
            cpnscek.save()
            # mkpns
            jarak = relativedelta(pnscek.tanggal, cpnscek.tanggal)
            pnscek.mk_tahun = jarak.years + cpnscek.mk_tahun
            pnscek.mk_bulan = jarak.months + cpnscek.mk_bulan
            pnscek.save()
            if pangkatgolongan:
                for i in golongandasarfilter:
                    if pangkatgolongan.nama_id < 22:
                        jaraka1 = relativedelta(pangkatgolongan.tanggal, pnscek.tanggal)
                        pangkatgolongan.mk_tahun = jaraka1.years + cpnscek.mk_tahun
                        pangkatgolongan.mk_bulan = jaraka1.months + cpnscek.mk_bulan
                        pangkatgolongan.save()

                    elif pangkatgolongan.nama_id >= 22:
                        # print(pangkatgolongan.nama_id, pangkatgolongan.tanggal)
                        jarak2 = relativedelta(pangkatgolongan.tanggal, pnscek.tanggal)
                        pangkatgolongan.mk_tahun = (jarak2.years + pnscek.mk_tahun)-5
                        pangkatgolongan.mk_bulan = jarak2.months + pnscek.mk_bulan
                        pangkatgolongan.save()
                        if pangkatgolongan.mk_tahun < 0:
                            pangkatgolongan.mk_tahun = 0
                            pangkatgolongan.mk_bulan = 0
                            pangkatgolongan.save()
                        elif pangkatgolongan.mk_bulan >= 12:
                            bulanlebih = pangkatgolongan.mk_bulan - 12
                            pangkatgolongan.mk_bulan = bulanlebih
                            pangkatgolongan.mk_tahun = pangkatgolongan.mk_tahun + 1
                            pangkatgolongan.save()

        elif cpnscek.nama_id == 18:
            cpnscek.mk_tahun = 0
            cpnscek.mk_bulan = 0
            cpnscek.save()

            # mkpns
            jarak = relativedelta(pnscek.tanggal, cpnscek.tanggal)
            pnscek.mk_tahun = jarak.years + cpnscek.mk_tahun
            pnscek.mk_bulan = jarak.months + cpnscek.mk_bulan
            pnscek.save()

            # mkall
            if pangkatgolongan:
                for i in golongandasarfilter:
                    if pangkatgolongan.nama_id < 22:
                        jaraka1 = relativedelta(pangkatgolongan.tanggal, cpnscek.tanggal)
                        pangkatgolongan.mk_tahun = jaraka1.years + cpnscek.mk_tahun
                        pangkatgolongan.mk_bulan = jaraka1.months + cpnscek.mk_bulan
                        pangkatgolongan.save()

                    elif pangkatgolongan.nama_id >= 22:
                        jarak2 = relativedelta(pangkatgolongan.tanggal, pnscek.tanggal)
                        pangkatgolongan.mk_tahun = (jarak2.years + pnscek.mk_tahun)-5
                        pangkatgolongan.mk_bulan = jarak2.months + pnscek.mk_bulan
                        pangkatgolongan.save()
                        if pangkatgolongan.mk_tahun < 0:
                            pangkatgolongan.mk_tahun = 0
                            pangkatgolongan.mk_bulan = 0
                            pangkatgolongan.save()
                        elif pangkatgolongan.mk_bulan >= 12:
                            bulanlebih = pangkatgolongan.mk_bulan - 12
                            pangkatgolongan.mk_bulan = bulanlebih
                            pangkatgolongan.mk_tahun = pangkatgolongan.mk_tahun + 1
                            pangkatgolongan.save()

        else:
            cpnscek.mk_tahun = 0
            cpnscek.mk_bulan = 0
            cpnscek.save()

            # mkpsn
            jarak = relativedelta(pnscek.tanggal, cpnscek.tanggal)
            pnscek.mk_tahun = jarak.years + cpnscek.mk_tahun
            pnscek.mk_bulan = jarak.months + cpnscek.mk_bulan
            pnscek.save()

            # mkall
            if pangkatgolongan:
                jarak = relativedelta(pangkatgolongan.tanggal, cpnscek.tanggal)
                pangkatgolongan.mk_tahun = jarak.years + cpnscek.mk_tahun
                pangkatgolongan.mk_bulan = jarak.months + cpnscek.mk_bulan
                pangkatgolongan.save()
                if pangkatgolongan.mk_bulan >= 12:
                    bulanlebih = pangkatgolongan.mk_bulan - 12
                    pangkatgolongan.mk_bulan = bulanlebih
                    pangkatgolongan.mk_tahun = pangkatgolongan.mk_tahun + 1
                    pangkatgolongan.save()

    return redirect('pegawai:riwayatpangkat', data.nip)


def ProsesBerkalaView(request, id):
    request.session['username']
    tmtkgb = request.session['tmtkgb']
    pegawai = get_object_or_404(PegawaiModel, id=id)
    gol = get_object_or_404(GolonganModel, id=pegawai.golongan_id)
    datagol = GolonganHistoryModel.objects.filter(pengguna=pegawai.id).order_by('-tanggal').first()
    gaji = get_object_or_404(GajiModel, masa_kerja=datagol.mk_tahun, golongan_id=gol.id)
    tmt_kgb = datetime.datetime.strptime(tmtkgb, '%Y-%m-%d').date()
    jarak = relativedelta(tmt_kgb, datagol.tanggal)
    mkbarutahun = jarak.years + datagol.mk_tahun
    mkbarubulan = jarak.months + datagol.mk_bulan
    print(pegawai.opd_id, pegawai.golongan_id, gaji.id, pegawai.jabatan,datagol.mk_tahun, tmt_kgb, mkbarutahun, jarak.years, mkbarubulan, jarak.months)
    if mkbarubulan >= 12:
        mkbarubulan = mkbarubulan - 12
        mkbarutahun = mkbarutahun + 1

    NominatifxModels.objects.get_or_create(
        golongan_id=pegawai.golongan_id,
        gaji_id=gaji.id,
        jabatan=pegawai.jabatan,
        mk_tahun=datagol.mk_tahun,
        mk_bulan=datagol.mk_bulan,
        mkb_tahun=mkbarutahun,
        mkb_bulan=mkbarubulan,
        pegawai_id=pegawai.id,
        opd_id=pegawai.opd_id,
        tmt_kgb=tmt_kgb,
    )
    return redirect('pegawai:nominatif')


class NominatifManual(ListView):
    model = PegawaiModel
    ordering = ['tmt_cpns']
    template_name = 'pegawai/nominatifmanuallist.html'
    paginate_by = 25

    def get_queryset(self):
        self.request.session['username']
        opdakses = self.request.session['opd_akses']
        self.queryset = self.model.objects.filter(opd_id=opdakses)
        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, PegawaiModel):
                queryset = self.queryset.all()

        # elif self.model is not None:
        #     queryset = self.model._default_manager.all()
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {
                    'cls': self.__class__.__name__
                }
            )
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset


def CariManualNominatif(request):
    request.session['username']
    opdakses = request.session['opd_akses']
    queryset = PegawaiModel.objects.filter(opd_id=opdakses)
    cari = request.GET.get('search', '')
    if cari is not None and cari != '':
        caripegawai = PegawaiModel.objects.filter(
            opd_id=opdakses, nama__icontains=cari)
    else:
        return redirect('pegawai:pegawai')
    return render(request, 'pegawai/nominatifmanuallist.html', {'object_list': caripegawai})


def ProsesManualNominatif(request, id):
    template_name = 'pegawai/prosesnominatifmanual.html'
    pegawai = get_object_or_404(PegawaiModel, id=id)
    gol = get_object_or_404(GolonganModel, id=pegawai.golongan_id)
    golajuan = GolonganHistoryModel.objects.filter(pengguna=pegawai.id).order_by('-tanggal').first()
    gaji = get_object_or_404(GajiModel, masa_kerja=golajuan.mk_tahun, golongan_id=gol.id)
    
    context = {
        'pegawai': pegawai,
        'golongan': gol,
        'golajuan': golajuan
    }
    if request.method == 'POST':
        tmtkgb = request.POST.get('tmtkgb')
        tmtkgb = datetime.datetime.strptime(tmtkgb, '%Y-%m-%d').date()
        jarak = relativedelta(tmtkgb, golajuan.tanggal)
        mkbarutahun = jarak.years + golajuan.mk_tahun
        mkbarubulan = jarak.months + golajuan.mk_bulan
        if mkbarubulan >= 12:
            mkbarubulan = mkbarubulan - 12
            mkbarutahun = mkbarutahun + 1
            print(pegawai.opd_id, pegawai.golongan_id, gaji.id, pegawai.jabatan, tmtkgb, golajuan.mk_tahun, golajuan.mk_bulan, mkbarutahun, mkbarubulan, jarak.years, jarak.months)
            if mkbarutahun % 2 != 0 or mkbarubulan > 0 :
                return HttpResponse("Salah Input TMT KGB")
            else:
                NominatifxModels.objects.get_or_create(
                    golongan_id=pegawai.golongan_id,
                    gaji_id=gaji.id,
                    jabatan=pegawai.jabatan,
                    mk_tahun=golajuan.mk_tahun,
                    mk_bulan=golajuan.mk_bulan,
                    mkb_tahun=mkbarutahun,
                    mkb_bulan=mkbarubulan,
                    pegawai_id=pegawai.id,
                    opd_id=pegawai.opd_id,
                    tmt_kgb=tmtkgb
                    )
        else:
            NominatifxModels.objects.get_or_create(
                    golongan_id=pegawai.golongan_id,
                    gaji_id=gaji.id,
                    jabatan=pegawai.jabatan,
                    mk_tahun=golajuan.mk_tahun,
                    mk_bulan=golajuan.mk_bulan,
                    mkb_tahun=mkbarutahun,
                    mkb_bulan=mkbarubulan,
                    pegawai_id=pegawai.id,
                    opd_id=pegawai.opd_id,
                    tmt_kgb=tmtkgb
                    )
    return render(request, template_name, context)


class OpdListView(ListView):
    template_name = 'admin/uploadperopd.html'
    model = OpdModel

    def get_queryset(self, *args, **kwargs):
        qs = super(OpdListView, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("nama")
        return qs


def LoadPegawaiView(request, id=None):
    opd = OpdModel.objects.get(id=id)
    openjson = urllib.request.urlopen(urlcompany + str(opd.id))
    data = json.load(openjson)
    for pegawai in data:
        inputdata = PegawaiModel.objects.update_or_create(
            id=pegawai['id'],
            nama=pegawai['name'],
            nip=pegawai['nip'],
            pengguna=pegawai['user_id'],
            golongan_id=pegawai['golongan_id'],
            opd_id=pegawai['company_id'],
        )
        cekdata = PegawaiModel.objects.exclude(
            nip__isnull=False).exclude(nip__exact="").delete()
        print(cekdata)

    return redirect('pegawai:pegawai')


def UpdateDataPegawai(request, id):
    pegawai = get_object_or_404(PegawaiModel, id=id)
    openjson = urllib.request.urlopen(urlpegawai + str(pegawai.nip))
    data = json.load(openjson)
    for x in data:
        pegawai.update(
            golongan_id=x['golongan_id'],
            opd_id=x['company_id']
            )
        pegawai.save()
    return redirect('pegawai:detail', pegawai.id)


class SelesaiList(ListView):
    model = NominatifSelesaiModels
    ordering = ['tmt_kgb']
    template_name = "selesailist.html"

    def get_queryset(self):
        self.request.session['username']
        opdakses = self.request.session['opd_akses']
        queryset = self.model.objects.filter(opd=opdakses)
        for data in queryset:
            print(data.pegawai)
        return queryset


def SelesaiDetailView(request, id):
    request.session['username']
    opdakses = request.session['opd_akses']
    data = get_object_or_404(PegawaiModel, id=id)
    gol = get_object_or_404(GolonganModel, id =data.golongan_id)
    pangkat = get_object_or_404(GolonganHistoryModel, pengguna=data.id, nama_id=gol.id)
    nominatif = get_object_or_404(ProsesBerkalaModel, pegawai_id=data.id)
    gaji = get_object_or_404(GajiModel, id=nominatif.gaji_id)
    return render(request, "pegawai/detailproses.html", {'pangkat': pangkat,  'data': data, 'nom': nominatif, 'gaji': gaji})



def CetakSelesai(request, id):
    request.session['username']
    opdakses = request.session['opd_akses']
    template_path = 'pegawai/cetakpdf.html'
    pegawai = get_object_or_404(PegawaiModel, id=id)
    pangkat = get_object_or_404(GolonganHistoryModel, nama_id=pegawai.golongan, pengguna=pegawai.id)
    simbol = get_object_or_404(GolonganModel, id=pegawai.golongan_id)
    nominatif = get_object_or_404(NominatifSelesaiModels, pegawai_id=pegawai.id)
    gajibaru = get_object_or_404(GajiModel, golongan_id=pegawai.golongan, masa_kerja=nominatif.mkb_tahun)
    gajilama = get_object_or_404(GajiModel, golongan_id=pegawai.golongan, masa_kerja=nominatif.mk_tahun)
    opd = get_object_or_404(OpdModel, id=pegawai.opd_id)
    kgbnext = nominatif.tmt_kgb+relativedelta(years=+2)
    inputselesai = NominatifSelesaiModels.objects.create(
        golongan_id=nominatif.golongan_id,
        gaji_id=nominatif.gaji_id,
        jabatan=nominatif.jabatan,
        mk_tahun=nominatif.mk_tahun,
        mk_bulan=nominatif.mk_bulan,
        mkb_tahun=nominatif.mkb_tahun,
        mkb_bulan=nominatif.mkb_bulan,
        pegawai_id=nominatif.pegawai_id,
        opd_id=nominatif.opd_id,
        tmt_kgb=nominatif.tmt_kgb
        )
    nominatif.delete()
    print(inputselesai.id)
    # kepelaopd = get_object_or_404(PegawaiModel, id=opd.kepala_opd)
    context = {'nominatif': nominatif, 'data': pegawai, 'pangkat': pangkat,
               'gajibaru': gajibaru, 'gajilama': gajilama, 'kgbnext': kgbnext, 'simbol': simbol}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return HttpResponse(pisa_status)


def ProsesDetail(request, id):
    request.session['username']
    opdakses = request.session['opd_akses']
    data = get_object_or_404(PegawaiModel, id=id)
    gol = get_object_or_404(GolonganModel, id =data.golongan_id)
    pangkat = get_object_or_404(GolonganHistoryModel, pengguna=data.id, nama=data.golongan)
    nominatif = get_object_or_404(NominatifxModels, pegawai_id=data.id)
    gaji = get_object_or_404(GajiModel, id=nominatif.gaji_id)
    return render(request, "pegawai/detailnominatif.html", {'pangkat': pangkat,  'data': data, 'nom': nominatif, 'gaji': gaji})

def ProsesDetailPost(request, id):
    data = get_object_or_404(PegawaiModel, id = id)
    nominatif = get_object_or_404(NominatifxModels, pegawai_id = data.id)
    print(data.id)
    inputproses = ProsesBerkalaModel.objects.get_or_create(
        golongan_id=nominatif.golongan_id,
        gaji_id=nominatif.gaji_id,
        jabatan=nominatif.jabatan,
        mk_tahun=nominatif.mk_tahun,
        mk_bulan=nominatif.mk_bulan,
        mkb_tahun=nominatif.mkb_tahun,
        mkb_bulan=nominatif.mkb_bulan,
        pegawai_id=nominatif.pegawai_id,
        opd_id=nominatif.opd_id,
        tmt_kgb=nominatif.tmt_kgb
        )
    nominatif.delete()
    return redirect('pegawai:selesaidetail',data.id)
        

class NominatifManuallist(ListView):
    model = PegawaiModel
    ordering = ['tmt_cpns']
    template_name = 'pegawai/nominatifmanuallist.html'
    paginate_by = 25

    def get_queryset(self):
        self.request.session['username']
        opdakses = self.request.session['opd_akses']
        self.queryset = self.model.objects.filter(opd_id=opdakses)
        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, PegawaiModel):
                queryset = self.queryset.all()

        # elif self.model is not None:
        #     queryset = self.model._default_manager.all()
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {
                    'cls': self.__class__.__name__
                }
            )
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset

class ProsesBerkalaList(ListView):
    model = ProsesBerkalaModel
    ordering = ['tmt_kgb']
    template_name = "prosesberkalamodel_list.html"

    def get_queryset(self):
        self.request.session['username']
        opdakses = self.request.session['opd_akses']
        queryset = self.model.objects.filter(opd=opdakses)
        for data in queryset:
            print(data.pegawai)
        return queryset


def SelesaiDetail(request, id):
    request.session['username']
    opdakses = request.session['opd_akses']
    data = get_object_or_404(PegawaiModel, id=id)
    gol = get_object_or_404(GolonganModel, id =data.golongan_id)
    pangkat = get_object_or_404(GolonganHistoryModel, pengguna=data.id, nama=data.golongan)
    nominatif = get_object_or_404(ProsesBerkalaModel, pegawai_id=data.id)
    gaji = get_object_or_404(GajiModel, id=nominatif.gaji_id)
    return render(request, "pegawai/selesainominatif.html", {'pangkat': pangkat,  'data': data, 'nom': nominatif, 'gaji': gaji})