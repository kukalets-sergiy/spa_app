from django.urls import path

from .views import CommentListCreateAPIView, CommentDetailAPIView, CommentReplyAPIView

app_name = 'spa_comment_app'

urlpatterns = [
    path('', CommentListCreateAPIView.as_view(), name='comment-list-create'),
    path('<int:pk>/', CommentDetailAPIView.as_view(), name='comment-detail'),
    path('<int:pk>/reply/', CommentReplyAPIView.as_view(), name='comment-reply'),
]
