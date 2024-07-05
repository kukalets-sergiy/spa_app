from django.conf import settings
from django.db import models
from django.utils import timezone


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             related_name="comments")
    username = models.CharField(max_length=50)
    email = models.EmailField()
    home_page = models.URLField(blank=True, null=True)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    file = models.FileField(upload_to='comment_files/', null=True, blank=True,
                            help_text='Upload an image or text file.')

    def __str__(self):
        return self.text[:300]
