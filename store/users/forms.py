from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms
from users.models import EmailVerification
from users.models import User
import uuid
from datetime import timedelta
from django.utils.timezone import now


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите имя пользователя'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите пароль'}))

    class Meta:
        model = User
        fields = ['username', 'password']


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите имя'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите фамилию'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите имя пользователя'
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите адрес эл. почты'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите пароль'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Подтвердите пароль'
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=True)
        expiration = now() + timedelta(hours=24)
        code = uuid.uuid4()
        record = EmailVerification.objects.create(user=user, expiration=expiration, code=code)
        record.send_verification_email()
        return user  # возвращаем пользователя чтобы сработал метод save


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',  # стиль для поля
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', }))
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'custom-file-label'}), required=False)  # необязательно добавлять
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'readonly': True  # нельзя изменять
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'readonly': True
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'image', 'username', 'email']
