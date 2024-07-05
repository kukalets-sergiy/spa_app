import os
from celery import shared_task
from django.core.mail import send_mail
from spa_app_core import settings
from spa_comments_app.models import Comment


@shared_task
def send_notification_email(comment_id):
    try:
        comment = Comment.objects.get(pk=comment_id)
        subject = 'New Comment Notification'
        message = f'Hello Admin,\n\nA new comment has been posted:\n\n{comment.text}\n\nRegards,\nYour Website Team'
        from_email = settings.EMAIL_HOST_USER
        recipient = settings.CORPORATE_EMAIL

        send_mail(subject, message, from_email, [recipient])
        print(f"Email sent to {recipient} for comment ID: {comment_id}")
    except Comment.DoesNotExist:
        print(f"Comment with id {comment_id} does not exist.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
