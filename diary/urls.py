from django.urls import path
from . import views

app_name = 'diary'

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_entry, name='create_entry'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.profile, name='user_profile'),
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
    path('register/', views.register_view, name='register'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('delete-entry/<int:entry_id>/', views.delete_entry, name='delete_entry'),
]
