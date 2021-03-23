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
                except:
                    messages.add_message(request, messages.INFO, 'Akun ini belum terhubung dengan data karyawan, silahkan hubungi administrator')
                return redirect('pegawai:index')
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
    context = {
        'pegawai':pegawai
        }
    return render(request, 'pegawai/index.html', context )

@login_required()
def DetailView(request, id):
    template_name= 'pegawai/detail.html'
    request.session['username']
    opdakses = request.session['opd_akses']
    pegawai = get_object_or_404(PegawaiModel, id=id)
    pangkat = urllib.request.urlopen('http://202.179.184.151/riwayatpangkat/?search='+ str(pegawai.id))
    json_pangkat = json.load(pangkat)


    for pkt in json_pangkat:
        list_pkt = GolonganHistoryModel.objects.get_or_create(
            id =pkt['id'],
            pengguna = pkt['partner'],
            nama_id = pkt['golongan_id_history'],
            nip = pegawai.nip,
            jenis = pkt['jenis'],
            tanggal = pkt['date']
            )
    range_golongan = GolonganHistoryModel.objects.filter(pengguna=pkt['partner'])
    for x in range_golongan:
        tmt_cpns = get_object_or_404(GolonganHistoryModel, jenis = "cpns", pengguna=pkt['partner'])
        mk_tahun = relativedelta(x.tanggal, tmt_cpns.tanggal)
        mk_total = relativedelta(datetime.datetime.now(), tmt_cpns.tanggal)
        #print ("Total Masa Kerja", mk_total)
        print(mk_tahun.years, mk_tahun.months)
    akun = PegawaiModel.objects.filter(id=id).update(
        mk_tahun = mk_tahun.years,
        mk_bulan =mk_tahun.months,
        tmt_cpns=tmt_cpns.tanggal
        )
    # mk_tahun = mk_tahun.years,mk_bulan =mk_tahun.months, tmt_cpns=tmt_cpns.tanggal)
    # if akun.exists():
    #     (PegawaiModel.id=id).
    #         mk_tahun = mk_tahun.years,
    #         mk_bulan =mk_tahun.months
    #     )
    print(akun)

    return render(request, template_name, {'pegawai':pegawai, 'json_pangkat':json_pangkat, 'range_golongan':range_golongan})

def RiwayatPangkatView(request,id):
    request.session['username']
    opdakses = request.session['opd_akses']
    pegawai = get_object_or_404(PegawaiModel, id=id)
    return render(request,'pegawai/riwayatpangkat.html')

    
def RiwayatPangkatView(request):
    return render(request,'pegawai/riwayatpangkat.html')


# @login_required
# def UploadPegawai(request):
#     request.session['username']
#     opdakses = request.session['opd_akses']
#     pegawai = urllib.request.urlopen('http://202.179.184.151/nip/?company='+ str(opdakses))
#     list_pegawai = json.load(pegawai)
#     opd = OpdModel.objects.all()
#     for data in list_pegawai:
#         PegawaiModel.objects.get_or_create(
#             id=data['id'],
#             nama=data['name'],
#             #jabatan=data['jabatan_data'],
#             nip=data['nip'],
#             opd=data['company_id'],
#             pangkat=data['golongan_id'],
#             pengguna=data['user_id']
#             )
#         # AkunModel.objects.get_or_create(
#         #     akun =data['user_id'],
#         #     pegawai = data['id'],
#         #     jenis_akun = 'pegawai'
#         # ) 
#     return render(request, 'pegawai/uploadperopd.html',context={'json_str':list_pegawai, 'opd':opd})