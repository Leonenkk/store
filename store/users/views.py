from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from common.views import TitleMixin
from products.models import Basket
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from users.models import EmailVerification, User


class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('index')
    title = 'Store - Авторизация'


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    template_name = 'users/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:login')
    success_message = 'Вы зарегистрированы!'
    title = 'Store - Регистрация'


class UserProfileView(TitleMixin,UpdateView):
    model = User
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    title = 'Store - Профиль'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))

class EmailVerificationView(TitleMixin,TemplateView):
    template_name = 'users/email_verification.html'
    title = 'Store - Подтверждение электронной почты'

    def get(self,request,*args, **kwargs):
        code = kwargs['code']
        user=User.objects.get(email=kwargs['email'])
        email_verification=EmailVerification.objects.filter(user=user,code=code).first()
        if email_verification and not email_verification.is_expired():
            user.is_verified_email=True
            user.save()
            return super(EmailVerificationView,self).get(request,*args,**kwargs)
        else:
            return redirect(reverse('index'))
