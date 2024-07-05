import re
from django import forms
from spa_comments_app.models import Comment
from captcha.fields import CaptchaField
from user_management_app.serializers import User


class CommentForm(forms.ModelForm):
    captcha = CaptchaField(required=True)
    file = forms.FileField(required=False)

    class Meta:
        model = Comment
        fields = ['username', 'email', 'home_page', 'text', 'captcha', 'file']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CommentForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if self.request and hasattr(self.request, 'user') and isinstance(self.request.user, User):
            if username != self.request.user.username:
                raise forms.ValidationError("The username does not match your account.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.request and hasattr(self.request, 'user') and isinstance(self.request.user, User):
            if email != self.request.user.email:
                raise forms.ValidationError("The email does not match your account.")
        return email

    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha')
        return captcha


    def clean_home_page(self):
        home_page = self.cleaned_data.get('home_page')
        if home_page and not re.match(r'^https?://', home_page):
            raise forms.ValidationError("The URL should start with http:// or https://")
        return home_page
