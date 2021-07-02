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
    path('pegawai/detail/<int:id>', views.HitungPangkatView, name='detail'),
    path('pegawai/detail/update/<int:id>', views.UpdateDataPegawai, name='update'),  
    
    path('pegawai/daftarnominatif', views.NominatifViews, name='nominatif'),
    path('pegawai/daftarnominatif/list', views.NominatifList.as_view(), name='nominatiflist'),
    path('pegawai/daftarnominatif/detail/<int:id>', views.NominatifDetailView, name='nominatifdetail'),
    path('pegawai/daftarnominatif/proses/<int:id>/manual', views.ProsesManualNominatif, name='prosesnominatifmanual'),

    
    path('pegawai/daftarnominatif/selesai/', views.SelesaiList.as_view(), name='selesai'),
    path('pegawai/daftarnominatif/selesai/detail/<int:id>', views.SelesaiDetailView, name='selesaidetail'),
    
    path('pegawai/daftarnominatif/manual', views.NominatifManuallist.as_view(), name='listnominatifmanual'),
    path('pegawai/daftarnominatif/manual/cari', views.CariManualNominatif, name='carinominatifmanual'),
    
    path('pegawai/riwayatpangkat/<str:nip>', views.RiwayatPangkatView, name='riwayatpangkat'),    
    
    path('pegawai/prosesberkala/', views.ProsesBerkalaList.as_view(), name='berkalalist'),
    path('pegawai/prosesberkala/<int:id>', views.ProsesBerkalaView, name='prosesnominatif'), #Input Ke Nominatifxmodel 
    path('pegawai/prosesberkala/detail/<int:id>', views.ProsesDetail, name='prosesdetail'), #delete di Nominatifxmodel, input ke ProsesBerkalaModel
    
    
    path('pegawai/cetak/<int:id>',views.CetakPdfFile, name='cetakpdf'),
    path('pegawai/cetakselesai/<int:id>',views.CetakSelesai, name='cetakselesai'),
    path('pangkat/<int:id>', views.Hitungmasakerja, name='pangkat'),
    path('pegawai/opdlist/', views.OpdListView.as_view(), name='opd'),
    path('pegawai/opdlist/<int:id>', views.LoadPegawaiView, name='loadpegawai')
    
    # path('riwayatkgb', views.RiwayatKgbView, name='riwayatkgb'),
    # path('welcome', views.IndexView, name='welcome'),
    # path('uploaduser', views.UploadView, name='uploaduser'),
    # path('uploadpegawai', views.UploadPegawai, name='uploadpegawai'),
    # path('detail', views.DetailView, name = 'detail'),
    # path('peropd', views.PerOpdView, name = 'uploadperopd'),
   
]
