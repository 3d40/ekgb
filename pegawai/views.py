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


# Create your views here.

#alamat = 'http://202.179.184.151/'

# def LoginView(request):
#     form = UserLoginForm(request.POST or None)
#     if not form.is_valid():
#         return render(request, 'login/login.html')
#     else :
#         username = form.cleaned_data.get('username')
#         password = form.cleaned_data.get('password')
#         user = authenticate(username=username, password=password)
#         akun = get_object_or_404(AkunModel, akun_id= user.id)

#         request.session['username'] = username
#         request.session['opd_akses'] = akun.opd_akses
#         request.session['jenis_akun'] = akun.jenis_akun 
#         login(request, user)
#         context ={}
#     return render(request, 'pegawai/index.html', context)

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
    request.session['username']
    opdakses = request.session['opd_akses']
    pegawai = PegawaiModel.objects.get(id=id)
    form = DetailForm(instance=pegawai)
    context = {
        'form':form
    }
    print(context)
    return render(request, 'pegawai/detail.html', context)
