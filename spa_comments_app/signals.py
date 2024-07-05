import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Comment

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Comment)
def clear_comment_cache(sender, instance, **kwargs):
    cache.delete('comments_list')
    logger.info(f"Cache 'comments_list' cleared after saving comment {instance.pk}")
    print(f"Cache 'comments_list' cleared after saving comment {instance.pk}")

@receiver(post_delete, sender=Comment)
def clear_comment_cache_on_delete(sender, instance, **kwargs):
    cache.delete('comments_list')
    logger.info(f"Cache 'comments_list' cleared after deleting comment {instance.pk}")
    print(f"Cache 'comments_list' cleared after deleting comment {instance.pk}")
