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
                    return redirect('pegawai:index')
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
<<<<<<< HEAD
    json_pangkat = json.load(pangkat)
=======

    json_pangkat = json.load(pangkat)

>>>>>>> 07c1ed949029e742a377262f916420ff6f4997ee
    for pkt in json_pangkat:
        list_pkt = GolonganHistoryModel.objects.filter().update_or_create(
            id =pkt['id'],
            pengguna = pkt['partner'],
            nama_id = pkt['golongan_id_history'],
            nip = pegawai.nip,
            jenis = pkt['jenis'],
            tanggal = pkt['date']
            )
<<<<<<< HEAD
    range_pegawai = PegawaiModel.objects.filter(pengguna=pkt['partner'])
    range_golongan = GolonganHistoryModel.objects.filter(pengguna=pkt['partner']).order_by('-tanggal')
    # golonganPegawai = get_object_or_404(GolonganHistoryModel, pengguna=pkt['partner'])
    tmt_cpns = get_object_or_404(GolonganHistoryModel, jenis="cpns", pengguna=pkt['partner'])
    
    
    # Masa Kerja Golongan I dan II
    for x in range_golongan:
        
        tmt_cpns = get_object_or_404(GolonganHistoryModel, jenis="cpns", pengguna=x.pengguna)
    if tmt_cpns.nama_id < 22:
        GolonganHistoryModel.objects.filter(jenis="cpns", pengguna=x.pengguna).update(
            mk_tahun = 3,
            mk_bulan = 0)
    elif tmt_cpns.nama_id > 31:
        GolonganHistoryModel.objects.filter(jenis="cpns", pengguna=x.pengguna).update(
            mk_tahun = 3,
            mk_bulan = 0)
    else:
        GolonganHistoryModel.objects.filter(jenis="cpns", pengguna=x.pengguna).update(
            mk_tahun = 0,
            mk_bulan = 0)
    
    # Masa Kerja Golongan III
    for y in range_golongan:
        mk = relativedelta(y.tanggal, tmt_cpns.tanggal)
        print(mk.years, "Tahun", mk.months, "Bulan")
        if y.jenis != "cpns":
            y.mk_tahun = mk.years
            y.mk_bulan = mk.months
    
        
=======
    range_golongan = GolonganHistoryModel.objects.filter(pengguna=pkt['partner']).order_by('-tanggal')
    request.session['pegawai'] = pkt['partner']

    for x in range_golongan:
        tmt_cpns = get_object_or_404(GolonganHistoryModel, jenis = "cpns", pengguna=pkt['partner'])
        #mk = relativedelta(x.tanggal, tmt_cpns.tanggal)
        #print(mk.years, "Tahun", mk.months, "Bulan", x.nama)
        #mk_total = relativedelta(datetime.datetime.now(), tmt_cpns.tanggal)
        #print ("Total Masa Kerja", mk_total
        if tmt_cpns.nama_id < 565 :
            mk_cpns = relativedelta(tmt_cpns.tanggal, tmt_cpns.tanggal)
            mk_capeg = (mk_cpns.years)+3
            print(mk_capeg)
            mk = relativedelta(x.tanggal, tmt_cpns.tanggal)
            mk_all = (mk.years)+ mk_capeg
            masa = mk.years-5
            if masa < 1:
                q = masa + 5
                GolonganHistoryModel.objects.filter(pengguna=pkt['partner'], id = x.id).update(
                    mk_tahun = q,
                    mk_bulan = relativedelta(x.tanggal, tmt_cpns.tanggal).months
                    )
            else:
                GolonganHistoryModel.objects.filter(pengguna=pkt['partner'], id = x.id).update(
                    mk_tahun = relativedelta(x.tanggal, tmt_cpns.tanggal).years,
                    mk_bulan = relativedelta(x.tanggal, tmt_cpns.tanggal).months
                    )
    # akun = PegawaiModel.objects.filter(id=id).update(
    #     mk_tahun = mk_tahun.years,
    #     mk_bulan =mk_tahun.months,
    #     tmt_cpns=tmt_cpns.tanggal
    #     )
    # mk_tahun = mk_tahun.years,mk_bulan =mk_tahun.months, tmt_cpns=tmt_cpns.tanggal)
    # if akun.exists():
    #     (PegawaiModel.id=id).
    #         mk_tahun = mk_tahun.years,
    #         mk_bulan =mk_tahun.months
    #     )

>>>>>>> 07c1ed949029e742a377262f916420ff6f4997ee
    return render(request, template_name, {'pegawai':pegawai, 'json_pangkat':json_pangkat, 'range_golongan':range_golongan})

def RiwayatPangkatView(request,id):
    request.session['username']
    opdakses = request.session['opd_akses']
    pegawai = get_object_or_404(PegawaiModel, id=id)
    return render(request,'pegawai/riwayatpangkat.html')

    
def RiwayatPangkatView(request,id):
    request.session['username']
    opdakses = request.session['opd_akses']
    pegawai = get_object_or_404(PegawaiModel, id=id)
    list_pkt = GolonganHistoryModel.objects.filter(pengguna=pegawai.id)
    print(list_pkt)



    return render(request,'pegawai/riwayatpangkat.html',{'pegawai':pegawai, 'list_pkt':list_pkt})



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