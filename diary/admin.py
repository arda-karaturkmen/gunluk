from django.contrib import admin
from .models import UserProfile, Follow, DiaryEntry, DiaryPhoto

# Bu inline, fotoğrafları doğrudan DiaryEntry admin sayfasında yönetmeyi sağlar.
class DiaryPhotoInline(admin.TabularInline):
    model = DiaryPhoto
    extra = 1  # Yeni fotoğraf eklemek için 1 adet boş form göster
    max_num = 3 # En fazla 3 fotoğraf
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        from django.utils.html import format_html
        if obj.image:
            return format_html('<img src="{}" width="150" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Görsel Önizleme'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    search_fields = ['user__username', 'user__email']


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following', 'created_at']
    list_filter = ['created_at']
    search_fields = ['follower__username', 'following__username']


@admin.register(DiaryEntry)
class DiaryEntryAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'privacy', 'created_at')
    list_filter = ('privacy', 'created_at', 'author')
    search_fields = ('title', 'content', 'author__username')
    inlines = [DiaryPhotoInline] # Fotoğraf yöneticisini göm
    date_hierarchy = 'created_at'


@admin.register(DiaryPhoto)
class DiaryPhotoAdmin(admin.ModelAdmin):
    list_display = ('entry_title', 'image_preview', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('diary_entry__title', 'diary_entry__author__username')
    readonly_fields = ('image_preview',)

    def entry_title(self, obj):
        return obj.diary_entry.title
    entry_title.short_description = 'Günlük Girişi'

    def image_preview(self, obj):
        from django.utils.html import format_html
        if obj.image:
            return format_html('<img src="{}" width="150" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Görsel Önizleme'
