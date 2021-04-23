from django.shortcuts import render, get_object_or_404, redirect
from .forms import UserLoginForm
from django.contrib.auth import (
    authenticate,
    login,
    logout)
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
import csv, io
from .models import *
import urllib, json
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView
from . forms import *
import datetime
from dateutil.relativedelta import *
from django.core.exceptions import MultipleObjectsReturned
from itertools import zip_longest
from django.http import Http404
from django.views.generic import ListView, DetailView, View
from django.views.generic.detail import SingleObjectMixin
from .filter import FilterPegawai



# Create your views here.

urlpegawai = 'http://202.179.184.151/nip/?search='
urlcompany = 'http://202.179.184.151/nip/?company='
urlpangkat = 'http://202.179.184.151/riwayatpangkat/?search='

def LoginView(request):
    if request.POST:
        user = authenticate(username=request.POST['username'], password=request.POST['password']) 
        if user is not None:
            akun = AkunModel.objects.get(akun_id=user.id)
            request.session['opd_akses'] = akun.opd_akses.id
            if user.is_active:
                try:
                    request.session['username'] = request.POST['username']
                    login(request, user)
                    return redirect('pegawai:pegawai')
                except:
                    messages.add_message(request, messages.INFO, 'User belum terverifikasi')
            else:
                messages.add_message(request, messages.INFO, 'User belum terverifikasi')
        else:
            messages.add_message(request, messages.INFO, 'Username atau password Anda salah')
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
    pegawai = PegawaiModel.objects.filter(opd_id = opdakses)
    jumlah = len(pegawai)
    #cari TMT_CPNS
    for x in pegawai :
        tahun = int(x.nip[8:12])
        bulan = int(x.nip[12:14])
        tanggal = 1
        cpns = datetime.date(tahun,bulan,tanggal)
        print(cpns)
        q = get_object_or_404(PegawaiModel, id = x.id)
        q.tmt_cpns = cpns
        q.save()
    return render(request, 'pegawai/index.html', {'pegawai':pegawai})

@login_required()
def HitungPangkatView(request, id):
    template_name= 'pegawai/detail.html'
    request.session['username']
    opdakses = request.session['opd_akses']
    pegawai = get_object_or_404(PegawaiModel, id=id)
    pangkat = urllib.request.urlopen('http://202.179.184.151/riwayatpangkat/?search='+ str(pegawai.id))
    json_pangkat = json.load(pangkat)
    for pkt in json_pangkat:
        list_pkt = GolonganHistoryModel.objects.filter().update_or_create(
            id =pkt['id'],
            pengguna = pkt['partner'],
            nama_id = pkt['golongan_id_history'],
            nip = pegawai.nip,
            jenis = pkt['jenis'],
            tanggal = pkt['date']
            )
    range_pegawai = PegawaiModel.objects.filter(pengguna=pkt['partner'])
    range_golongan = GolonganHistoryModel.objects.filter(pengguna=pkt['partner']).order_by('-tanggal')
    return render(request, template_name, {'pegawai':pegawai, 'json_pangkat':json_pangkat, 'range_golongan':range_golongan})
    
def RiwayatPangkatView(request, nip):
    request.session['username']
    opdakses = request.session['opd_akses']
    pangkat = GolonganHistoryModel.objects.filter(nip=nip).order_by('-tanggal')
    pegawai = get_object_or_404(PegawaiModel,nip=nip)
    return render (request,'pegawai/riwayatpangkat.html',{'object_list':pangkat, 'pegawai':pegawai})
    

def NominatifViews(request):
    request.session['username']
    opdakses = request.session['opd_akses']
    pegawai = PegawaiModel.objects.filter(opd_id = opdakses)
    pangkat = GolonganHistoryModel.objects.filter(jenis='cpns')
    jumlah = len(pegawai)
    #cari TMT_CPNS
    tmtkgb_post = request.POST.get('tmtkgb')
    for x in pegawai:
        tahun = int(x.nip[8:12])
        bulan = int(x.nip[12:14])
        tanggal = 1
        cpns = datetime.date(tahun,bulan,tanggal)
        if request.POST:
            tmtkgb_date = datetime.datetime.strptime(tmtkgb_post, '%Y-%m-%d').date()
            nominasi = relativedelta(tmtkgb_date, x.tmt_cpns)
            mk_tahun = nominasi.years
            mk_bulan = nominasi.months
            if nominasi.years %2 == 0 and nominasi.months == 0:    
                pegnom = PegawaiModel.objects.filter(tmt_cpns= x.tmt_cpns)
                return render(request, 'pegawai/daftarnominatif.html',{
                    'object_list':pegnom, 
                    'mk_tahun':mk_tahun, 
                    'mk_bulan':mk_bulan, 
                    'tmtkgb_date':tmtkgb_date
                    })
            else:
                object_list = pegawai          
    return render(request, 'pegawai/daftarnominatif.html')


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

        elif self.model is not None:
            queryset = self.model._default_manager.all()
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
        caripegawai = PegawaiModel.objects.filter(opd_id=opdakses, nama__icontains = cari )
    else:
        return redirect ('pegawai:pegawai')
    return render(request, 'pegawai/caripegawai_list.html', {'object_list': caripegawai})