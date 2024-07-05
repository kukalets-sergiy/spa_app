from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Comment


@receiver(post_save, sender=Comment)
def update_comment_cache(sender, instance, **kwargs):
    cache_key = f'comment_detail_{instance.pk}'
    cache.set(cache_key, instance, timeout=60 * 15)


@receiver(post_delete, sender=Comment)
def delete_comment_cache(sender, instance, **kwargs):
    cache_key = f'comment_detail_{instance.pk}'
    cache.delete(cache_key)
