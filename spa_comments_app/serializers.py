import re
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from .models import Comment
from rest_framework import serializers
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


def validate_tags(value):
    allowed_tags = {'a', 'code', 'i', 'strong'}
    pattern = r'<(?:a href="[^"]*" title="[^"]*")|(/?code|/?i|/?strong)>'
    tags = re.findall(r'<(\/?[^ >]+)', value)
    for tag in tags:
        tag_name = tag.strip('/')
        if tag_name not in allowed_tags:
            raise ValidationError(f"Tag <{tag}> is not allowed.")


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    file = serializers.FileField(required=False)

    class Meta:
        model = Comment
        fields = ['id', 'username', 'email', 'home_page', 'text', 'date', 'parent', 'replies', 'file']

    def validate_text(self, value):
        validate_tags(value)
        return value

    def validate_file(self, value):
        if value:
            max_file_size = 100 * 1024  # 100 KB
            allowed_image_formats = ['jpg', 'jpeg', 'png', 'gif']
            allowed_text_formats = ['txt']

            file_extension = value.name.split('.')[-1].lower()
            file_size = value.size

            if file_extension in allowed_image_formats:
                if file_size > max_file_size:
                    raise serializers.ValidationError(f"Image file size exceeds {max_file_size} bytes.")

                # Validate image dimensions
                image = Image.open(value)
                if image.width > 320 or image.height > 240:
                    output_size = (320, 240)
                    image.thumbnail(output_size)
                    buffer = BytesIO()
                    image.save(buffer, format=image.format)
                    value = InMemoryUploadedFile(buffer, None, value.name, value.content_type,
                                                 buffer.tell(), None)

            elif file_extension in allowed_text_formats:
                if file_size > max_file_size:
                    raise serializers.ValidationError(f"Text file size exceeds {max_file_size} bytes.")
            else:
                raise serializers.ValidationError("Unsupported file format.")

        return value

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user if request.user.is_authenticated else None
        else:
            validated_data['user'] = None

        return super().create(validated_data)

    def get_replies(self, obj):
        request = self.context.get('request', None)
        page_size = 25
        page_number = 1

        if request is not None:
            page_size = int(request.query_params.get('reply_page_size', 25))
            page_number = request.query_params.get('reply_page', 1)

        replies = obj.replies.all().order_by('-date')
        paginator = Paginator(replies, page_size)
        page_obj = paginator.get_page(page_number)
        serializer = CommentSerializer(page_obj, many=True, context={'request': request})

        total_replies = paginator.count
        total_comments_and_replies = obj.replies.count() + 1

        return {
            'replies': serializer.data,
            'page': page_obj.number,
            'num_pages': paginator.num_pages,
            'total_replies': total_replies,
            'total_comments_and_replies': total_comments_and_replies,
        }

    def validate(self, data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            if data['username'] != request.user.username or data['email'] != request.user.email:
                raise serializers.ValidationError("The username or email does not match your account.")
        return data
