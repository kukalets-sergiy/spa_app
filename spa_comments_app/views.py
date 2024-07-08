from django.core.cache import cache
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from spa_app_core.utils import count_all_comments_and_replies
from .forms import CommentForm
from .models import Comment
from .serializers import CommentSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .tasks import send_notification_email
from django.shortcuts import render


class CommentListCreateAPIView(APIView):
    form_class = CommentForm
    template_name = 'user_management/homepage.html'
    queryset = Comment.objects.filter(parent__isnull=True)
    serializer_class = CommentSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    ordering_fields = {
        'username': 'user__username',
        'email': 'user__email',
        'date': 'date',
    }

    def get_queryset(self):
        order_by = self.request.query_params.get('order_by', '-date')
        if order_by in self.ordering_fields:
            return self.queryset.order_by(self.ordering_fields[order_by])
        elif order_by.startswith('-') and order_by[1:] in self.ordering_fields:
            return self.queryset.order_by('-' + self.ordering_fields[order_by[1:]])
        return self.queryset.order_by('-date')

    def get(self, request, *args, **kwargs):
        comments = self.get_queryset()
        page_size = int(request.GET.get('page_size', 14))
        paginator = Paginator(comments, page_size)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        serialized_comments = []
        total_comments_and_replies = 0

        for comment in page_obj:
            serialized_comment = CommentSerializer(comment, context={'request': request}).data
            total_comments_and_replies += comment.replies.count() + 1
            if total_comments_and_replies <= 25:
                serialized_comments.append(serialized_comment)
            else:
                break

        form = self.form_class()
        form_html = render(request, self.template_name, {'form': form}).content.decode('utf-8')
        response_data = {
            'comment_form_html': form_html,
            'comments': serialized_comments,
            'page': page_obj.number,
            'num_pages': paginator.num_pages,
            'total_comments_and_replies': total_comments_and_replies,
        }
        return Response(response_data)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, request=request)
        if form.is_valid():
            comment = form.save()
            send_notification_email.delay(comment.id)
            comments = self.get_queryset()
            page_size = int(request.GET.get('page_size', 25))
            paginator = Paginator(comments, page_size)
            page_number = request.GET.get('page', 1)
            page_obj = paginator.get_page(page_number)

            serialized_comments = []
            total_comments_and_replies = 0

            for comment in page_obj:
                serialized_comment = CommentSerializer(comment, context={'request': request}).data
                total_comments_and_replies += comment.replies.count() + 1
                if total_comments_and_replies <= 25:
                    serialized_comments.append(serialized_comment)
                else:
                    break

            return render(request, self.template_name,
                          {'form': self.form_class(request=request), 'comments': serialized_comments})
        else:
            comments = self.get_queryset()
            paginator = Paginator(comments, 25)
            page_number = request.GET.get('page', 1)
            page_obj = paginator.get_page(page_number)
            serializer = CommentSerializer(page_obj, many=True, context={'request': request})
            return render(request, self.template_name, {'form': form, 'comments': serializer.data})


class CommentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        cache_key = f'comment_detail_{pk}'
        comment = cache.get(cache_key)
        if not comment:
            comment = get_object_or_404(Comment, pk=pk)
            cache.set(cache_key, comment, timeout=60 * 15)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        if comment.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            updated_comment = serializer.save()
            cache.set(f'comment_detail_{pk}', updated_comment, timeout=60 * 15)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        if comment.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        cache.delete(f'comment_detail_{pk}')
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentReplyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        parent_comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            reply = serializer.save(user=request.user, parent=parent_comment)
            send_notification_email.delay(reply.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
