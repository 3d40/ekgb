from django.urls import path, include
from . import views
from . models import PegawaiModel
from django.views.generic import ListView

app_name = 'pegawai'
urlpatterns = [
    path('', views.LoginView, name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('pegawai/', views.Pegawai.as_view(), name = 'pegawai'),
    path('pegawai/cari/', views.CariView, name = 'cari'),
    path('pegawai/detail/<int:id>/', views.HitungPangkatView, name='detail'),  
    path('pegawai/daftarnominatif', views.NominatifViews, name='nominatif'),
    path('pegawai/riwayatpangkat/<str:nip>', views.RiwayatPangkatView, name='riwayatpangkat'),    
    # path('index', views.IndexView, name='index'),
    # path('riwayatkgb', views.RiwayatKgbView, name='riwayatkgb'),
    # path('welcome', views.IndexView, name='welcome'),
    # path('uploaduser', views.UploadView, name='uploaduser'),
    # path('uploadpegawai', views.UploadPegawai, name='uploadpegawai'),
    # path('detail', views.DetailView, name = 'detail'),
    # path('peropd', views.PerOpdView, name = 'uploadperopd'),
   
]
