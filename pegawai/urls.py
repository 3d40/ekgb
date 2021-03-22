from django.urls import path, include
from . import views

app_name = 'pegawai'
urlpatterns = [
    path('', views.LoginView, name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('index/', views.IndexView, name='index'),
    path('detail/<int:id>', views.DetailView, name='detail')
    # path('welcome', views.IndexView, name='welcome'),
    # path('uploaduser', views.UploadView, name='uploaduser'),
    # path('uploadpegawai', views.UploadView, name='uploadpegawai'),
    # path('detail', views.DetailView, name = 'detail'),
    # path('peropd', views.PerOpdView, name = 'uploadperopd'),
    # path('riwawatkgb', views.RiwayatKgbView, name='riwayatkgb'),
    # path('riwayatpangkat', views.RiwayatPangkatView, name='riwayatpangkat')
]
