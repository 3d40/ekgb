from django import forms
from django.contrib.auth import authenticate
from . models import *


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('This user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')
        return super(UserLoginForm, self).clean(*args, **kwargs)
    
class GolonganHistoryForm(forms.ModelForm):
    class Meta:
        models = GolonganHistoryModel
        fields = ['nama','nomor_sk','tanggal','mk_tahun','mk_bulan']
    

class NominatifForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NominatifForm, self).__init__(*args, **kwargs)
        self.fields['pegawai'].disabled = True,
        self.fields['opd'].disabled = True
    
    class Meta:
        model = NominatifxModels
        fields = '__all__'
