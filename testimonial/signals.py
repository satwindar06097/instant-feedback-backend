from django.db.models.signals import pre_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from .models import Review

# Existing signal to update the username to email
@receiver(pre_save, sender=User)
def updateUser(sender, instance, **kwargs):
    user = instance
    if user.email != '':
        user.username = user.email

# New signal to delete associated files when a review is deleted
@receiver(post_delete, sender=Review)
def delete_review_files(sender, instance, **kwargs):
    if instance.customer_photo:
        instance.customer_photo.delete(save=False)
    if instance.review_image:
        instance.review_image.delete(save=False)
    if instance.video_review:
        instance.video_review.delete(save=False)
