from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):
        # First, call the original save method
        super().save(*args, **kwargs)

        # Then, process the image if it exists
        if self.profile_picture and self.profile_picture.name:
            try:
                # Dosya yolu elde edilebiliyorsa
                if hasattr(self.profile_picture.storage, 'path'):
                    img_path = self.profile_picture.path
                    img = Image.open(img_path)

                    # Resize if the image is larger than 300x300
                    if img.height > 300 or img.width > 300:
                        output_size = (300, 300)
                        img.thumbnail(output_size)
                        
                        # Save the image back to the same path
                        img.save(img_path, quality=85, optimize=True)
                # Dosya yolu elde edilemiyorsa (örn. S3 veya başka bir storage)
                else:
                    # Dosyayı belleğe al, işle ve geri kaydet
                    img_data = self.profile_picture.read()
                    img = Image.open(BytesIO(img_data))
                    
                    if img.height > 300 or img.width > 300:
                        output_size = (300, 300)
                        img.thumbnail(output_size)
                        
                        output = BytesIO()
                        img.save(output, format=img.format, quality=85, optimize=True)
                        output.seek(0)
                        
                        # Dosyayı güncelle
                        self.profile_picture.save(
                            self.profile_picture.name,
                            ContentFile(output.read()),
                            save=False
                        )
            except (IOError, FileNotFoundError, AttributeError):
                # Handle cases where the file might not exist or is corrupted
                pass


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('follower', 'following')
    
    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"


class DiaryEntry(models.Model):
    PRIVACY_CHOICES = [
        ('private', 'Sadece Ben'),
        ('public', 'Herkes'),
    ]
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diary_entries')
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='private')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Diary Entries'
    
    def __str__(self):
        return f"{self.author.username} - {self.created_at.strftime('%Y-%m-%d')}"
    
    @property
    def date_only(self):
        return self.created_at.date()


class DiaryPhoto(models.Model):
    diary_entry = models.ForeignKey(DiaryEntry, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='diary_photos/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Photo for {self.diary_entry}"

    def save(self, *args, **kwargs):
        # First, call the original save method
        super().save(*args, **kwargs)

        # Then, process the image if it exists
        if self.image and hasattr(self.image.storage, 'path'):
            try:
                img_path = self.image.path
                img = Image.open(img_path)

                # Resize if the image is larger than 1024x1024
                if img.height > 1024 or img.width > 1024:
                    output_size = (1024, 1024)
                    img.thumbnail(output_size)
                    
                    # Save the image back to the same path
                    img.save(img_path, quality=85, optimize=True)
            except (IOError, FileNotFoundError):
                # Handle cases where the file might not exist or is corrupted
                pass
