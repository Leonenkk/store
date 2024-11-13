from django.shortcuts import render,HttpResponseRedirect
from django.contrib import auth,messages #auth для входа/выхода, messages-для личных сообщений
from users.models import User
from users.forms import UserLoginForm, UserRegistrationForm,UserProfileForm
from django.urls import reverse


def login(request):
    if request.method == 'POST':# метод POST для ввода данных, GET для получения
        form = UserLoginForm(data=request.POST)#для изменения формы
        if form.is_valid():
            username=request.POST['username']
            password=request.POST['password']
            user=auth.authenticate(username=username,password=password)#для проверки на то, существует ли пользователь
            if user:
                auth.login(request,user)#вход
                return HttpResponseRedirect(reverse('index'))
    else:
        form=UserLoginForm()
    context = {'form':form}
    return render(request, 'users/login.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Аккаунт зарегистрирован')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {'form':form}
    return render(request, 'users/register.html',context)


def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user,data=request.POST,files=request.FILES)#files для добавления файлов
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))#reverse переводит на указанную страницу
        else:
            print(form.errors)
    else:
        form=UserProfileForm(instance=request.user)#для работы с текущем пользователем
    context={
        'title':'Store - Профиль',
        'form':form,
    }
    return render(request, 'users/profile.html',context)

def logout(request):
    auth.logout(request)#выход из системы
    return HttpResponseRedirect(reverse('index'))