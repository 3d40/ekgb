from django.urls import path, include
from . import views
from . models import PegawaiModel
from django.views.generic import ListView

app_name = 'pegawai'
urlpatterns = [
    path('', views.LoginView, name='login'),
    path('logout', views.LogoutView, name='logout'),
    path('pegawai', views.Pegawai.as_view(), name = 'pegawai'),
    path('pegawai/index', views.IndexView, name='index'),
    path('pegawai/cari', views.CariView, name = 'cari'),
    path('pegawai/detail/<str:id>', views.HitungPangkatView, name='detail'),  
    path('pegawai/daftarnominatif', views.NominatifViews, name='nominatif'),
    path('pegawai/daftarnominatif/list', views.NominatifList.as_view(), name='nominatiflist'),
    path('pegawai/daftarnominatif/detail/<int:pengguna>', views.NominatifDetailView, name='nominatifdetail'),
    path('pegawai/riwayatpangkat/<str:nip>', views.RiwayatPangkatView, name='riwayatpangkat'),    
    path('pegawai/prosesberkala/<int:pengguna>', views.ProsesBerkalaView, name='proses'),
    # path('index', views.IndexView, name='index'),
    # path('riwayatkgb', views.RiwayatKgbView, name='riwayatkgb'),
    # path('welcome', views.IndexView, name='welcome'),
    # path('uploaduser', views.UploadView, name='uploaduser'),
    # path('uploadpegawai', views.UploadPegawai, name='uploadpegawai'),
    # path('detail', views.DetailView, name = 'detail'),
    # path('peropd', views.PerOpdView, name = 'uploadperopd'),
   
]
