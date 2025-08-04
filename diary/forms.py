from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import DiaryEntry, UserProfile
import re


class DiaryEntryForm(forms.ModelForm):
    class Meta:
        model = DiaryEntry
        fields = ['title', 'content', 'privacy']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Başlık (opsiyonel)'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Bugün nasıl geçti? Ne düşünüyorsun?',
                'rows': 8
            }),
            'privacy': forms.Select(attrs={
                'class': 'form-control'
            })
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Kendinizden bahsedin...',
                'rows': 4
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'E-posta adresinizi girin'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Adınız (opsiyonel)'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Soyadınız (opsiyonel)'
        })
    )
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove username field from form
        if 'username' in self.fields:
            del self.fields['username']
        
        # Update password field widgets
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Güçlü bir şifre oluşturun'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Şifrenizi tekrar girin'
        })
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Bu e-posta adresi zaten kullanılıyor.')
        return email
    
    def generate_username_from_email(self, email):
        """Email'den benzersiz kullanıcı adı oluştur"""
        # Email'in @ işaretinden önceki kısmını al
        base_username = email.split('@')[0]
        # Özel karakterleri temizle
        base_username = re.sub(r'[^a-zA-Z0-9]', '', base_username)
        # En az 3 karakter olsun
        if len(base_username) < 3:
            base_username = 'user' + base_username
        
        username = base_username
        counter = 1
        
        # Benzersiz kullanıcı adı bulana kadar dene
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        
        return username
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        
        # Email'den kullanıcı adı oluştur
        user.username = self.generate_username_from_email(user.email)
        
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label='E-posta',
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'E-posta adresinizi girin'
        })
    )
    password = forms.CharField(
        label='Şifre',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Şifrenizi girin'
        })
    )
    
    def clean_username(self):
        email = self.cleaned_data.get('username')
        try:
            # Email ile kullanıcıyı bul
            user = User.objects.get(email=email)
            return user.username  # Gerçek username'i döndür
        except User.DoesNotExist:
            raise forms.ValidationError('Bu e-posta adresi ile kayıtlı kullanıcı bulunamadı.')


class EditUsernameForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Yeni kullanıcı adınız'
        }),
        help_text='Harf, rakam ve @/./+/-/_ karakterleri kullanabilirsiniz.'
    )
    
    class Meta:
        model = User
        fields = ['username']
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Mevcut kullanıcının username'i değilse ve başka biri kullanıyorsa hata ver
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Bu kullanıcı adı zaten kullanılıyor.')
        return username
