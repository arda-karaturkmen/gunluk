from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from .models import DiaryEntry, DiaryPhoto, UserProfile, Follow
from .forms import DiaryEntryForm, UserProfileForm, CustomUserCreationForm, CustomAuthenticationForm, EditUsernameForm
import json


def home(request):
    """Ana sayfa akışı"""
    if request.user.is_authenticated:
        following_users = list(Follow.objects.filter(follower=request.user).values_list('following_id', flat=True))
        
        # Kullanıcının kendi gönderilerini her zaman dahil et
        user_entries_q = Q(author=request.user)
        
        # Takip edilen kullanıcıların herkese açık gönderileri için Q nesnesi
        following_entries_q = Q(author__in=following_users, privacy='public')

        # Birleşik sorgu
        combined_q = user_entries_q | following_entries_q
        entries = DiaryEntry.objects.filter(combined_q).distinct().select_related('author', 'author__userprofile').prefetch_related('photos').order_by('-created_at')

        # Eğer kullanıcının akışı (kendi gönderileri hariç) boşsa, genel herkese açık gönderileri göster
        has_followed_content = entries.exclude(author=request.user).exists()
        if not has_followed_content:
            # Genel herkese açık gönderileri de akışa ekle
            public_entries_q = Q(privacy='public')
            final_q = user_entries_q | public_entries_q
            entries = DiaryEntry.objects.filter(final_q).distinct().select_related('author', 'author__userprofile').prefetch_related('photos').order_by('-created_at')

        paginator = Paginator(entries, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'diary/home.html', {'page_obj': page_obj})
    else:
        # Giriş yapmamış kullanıcılar için en son herkese açık gönderiler
        public_entries = DiaryEntry.objects.filter(privacy='public').select_related('author', 'author__userprofile').prefetch_related('photos').order_by('-created_at')[:20]
        return render(request, 'diary/landing.html', {'entries': public_entries})


@login_required
def create_entry(request):
    """Yeni günlük girişi oluştur"""
    if request.method == 'POST':
        form = DiaryEntryForm(request.POST)
        photos = request.FILES.getlist('photos')

        if len(photos) > 3:
            messages.error(request, 'En fazla 3 fotoğraf yükleyebilirsiniz.')
            return render(request, 'diary/create_entry.html', {'form': form})

        if form.is_valid():
            entry = form.save(commit=False)
            entry.author = request.user
            entry.save()  # Önce ana nesneyi kaydet

            # Sonra fotoğrafları işle
            for photo_file in photos:
                DiaryPhoto.objects.create(diary_entry=entry, image=photo_file)
            
            messages.success(request, 'Günlük girişiniz başarıyla oluşturuldu!')
            return redirect('diary:user_profile', username=request.user.username)
    else:
        form = DiaryEntryForm()
    
    return render(request, 'diary/create_entry.html', {'form': form})


@login_required
def profile(request, username=None):
    """Profil sayfası - kendi veya başkasının günlükleri"""
    if username:
        user = get_object_or_404(User, username=username)
        is_own_profile = user == request.user
    else:
        user = request.user
        is_own_profile = True
    
    # Profil bilgilerini al veya oluştur
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    # Günlük girişlerini filtrele
    if is_own_profile:
        entries = DiaryEntry.objects.filter(author=user)
    else:
        entries = DiaryEntry.objects.filter(author=user, privacy='public')
    
    entries = entries.select_related('author').prefetch_related('photos')
    
    # Takip durumunu kontrol et
    is_following = False
    if not is_own_profile and request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, following=user).exists()
    
    # Takvim görünümü için günlükleri tarihe göre grupla
    entries_by_date = {}
    for entry in entries:
        date_key = entry.date_only
        if date_key not in entries_by_date:
            entries_by_date[date_key] = []
        entries_by_date[date_key].append(entry)
    
    context = {
        'profile_user': user,
        'profile': profile,
        'entries': entries,
        'entries_by_date': entries_by_date,
        'is_own_profile': is_own_profile,
        'is_following': is_following,
    }
    
    return render(request, 'diary/profile.html', context)


@login_required
def follow_user(request, username):
    """Kullanıcıyı takip et/takibi bırak"""
    if request.method == 'POST':
        user_to_follow = get_object_or_404(User, username=username)
        
        if user_to_follow == request.user:
            return JsonResponse({'error': 'Kendinizi takip edemezsiniz.'}, status=400)
        
        follow_obj, created = Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )
        
        if not created:
            follow_obj.delete()
            is_following = False
        else:
            is_following = True
        
        return JsonResponse({'is_following': is_following})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


def register_view(request):
    """Kullanıcı kayıt sayfası - Email tabanlı"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # UserProfile oluştur
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, f'Hoş geldin! Kullanıcı adın: {user.username}')
            return redirect('diary:home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})


@login_required
def edit_profile(request):
    """Profil düzenleme sayfası"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        username_form = EditUsernameForm(request.POST, instance=request.user)
        
        if profile_form.is_valid() and username_form.is_valid():
            profile_form.save()
            username_form.save()
            messages.success(request, 'Profiliniz başarıyla güncellendi!')
            return redirect('diary:user_profile', username=request.user.username)
    else:
        profile_form = UserProfileForm(instance=profile)
        username_form = EditUsernameForm(instance=request.user)
    
    return render(request, 'diary/edit_profile.html', {
        'profile_form': profile_form,
        'username_form': username_form
    })


@login_required
def delete_entry(request, entry_id):
    """Günlük girişini sil"""
    entry = get_object_or_404(DiaryEntry, id=entry_id, author=request.user)
    
    if request.method == 'POST':
        entry.delete()
        messages.success(request, 'Günlük girişiniz silindi.')
        return redirect('diary:user_profile', username=request.user.username)
    
    return render(request, 'diary/delete_entry.html', {'entry': entry})
