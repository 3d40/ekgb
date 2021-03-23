from django.urls import path, include
from . import views

app_name = 'pegawai'
urlpatterns = [
    path('', views.LoginView, name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('index/', views.IndexView, name='index'),
    path('detail/<int:id>/', views.DetailView, name='detail'),  
    path('riwayatpangkat/<int:id>', views.RiwayatPangkatView, name='riwayatpangkat'),
    #path('riwayatkgb', views.RiwayatKgbView, name='riwayatkgb'),
    # path('welcome', views.IndexView, name='welcome'),
    # path('uploaduser', views.UploadView, name='uploaduser'),
    #path('uploadpegawai', views.UploadPegawai, name='uploadpegawai'),
    # path('detail', views.DetailView, name = 'detail'),
    # path('peropd', views.PerOpdView, name = 'uploadperopd'),
   
]
