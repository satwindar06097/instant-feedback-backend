from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import uuid
from django.utils.text import slugify
from django_resized import ResizedImageField
from cloudinary_storage.storage import VideoMediaCloudinaryStorage
from cloudinary_storage.validators import validate_video

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = ResizedImageField( quality=80,upload_to='images/', null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) + '-' + str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})
    
        
class Review(models.Model):
    post = models.ForeignKey(Post, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    my_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=255, null=True, blank=True)
    customer_email = models.EmailField(null=True, blank=True)
    customer_photo = ResizedImageField(  quality=80,upload_to='customer_images/', null=True, blank=True)
    review_image = ResizedImageField( quality=80,upload_to='review_images/', null=True, blank=True)
    text_review = models.TextField(null=True, blank=True)
    video_review = models.FileField(upload_to='review_videos/', null=True, blank=True,storage=VideoMediaCloudinaryStorage(),validators=[validate_video])
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.customer_name 
    