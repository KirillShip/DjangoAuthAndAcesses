from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import UserLoginForm, UserRegistrationForm, UserUpdateForm
from admin.forms import ElementSelectForm
from .models import User, Session, Element, Permission
import datetime

def index(request):
    return redirect('main')

def login(request):
    error = ""
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['user_email']
            password = form.cleaned_data['user_password']
            email_exist = User.objects.filter(user_email=email, is_active=True).exists()
            if email_exist:
                existing_user = User.objects.get(user_email=email)
                if check_password(password, existing_user.user_password):
                    session = Session(
                        user_id=existing_user,
                        expires_at=timezone.now() + datetime.timedelta(days=1),
                    )
                    session.save()
                    response = redirect('main')
                    response.set_cookie('user_id', existing_user.pk, max_age=24*60*60, secure=True)
                    response.set_cookie('session_id', session.session_id, max_age=24*60*60, secure=True)
                    return response
                else:
                    error = "Введен неправильный пароль"
            else:
                error = "Пользователя с такой почтой не существует"
        else:
            error = "Неправильно заполнена форма"
    form = UserLoginForm(request.POST)
    data = {
        'form': form,
        'error': error
    }
    return render(request,'account/login.html', data)


def registration(request):
    error = ""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['user_name']
            password = form.cleaned_data['user_password']
            password_confirm = form.cleaned_data['password_confirm']
            email = form.cleaned_data['user_email']
            hashed_password = make_password(password)
            email_exist = User.objects.filter(user_email=email).exists()
            if email_exist:
                error = "Пользователь с такой почтой уже существует"
            elif password != password_confirm:
                error = "Пароли не совпадают"
            else:
                new_user = User(
                    user_name=name,
                    user_email=email,
                    user_password=hashed_password
                )
                new_user.save()
                return redirect('login')
        else:
            error = "Неправильно заполнена форма"

    form = UserRegistrationForm(request.POST)
    data = {
        'form': form,
        'error': error
    }
    return render(request,'account/registration.html', data)


def logout(request):
    session_id = request.COOKIES.get('session_id')
    response = redirect('login')
    response.delete_cookie('session_id')
    response.delete_cookie('user_id')
    try:
        Session.objects.filter(session_id=session_id).delete()
    except Session.DoesNotExist:
        pass
    return response


def delete(request):
    user_id = request.COOKIES.get('user_id')
    session_id = request.COOKIES.get('session_id')
    response = redirect('login')
    user = User.objects.get(pk=user_id)
    user.is_active = False
    user.save()
    response.delete_cookie('session_id')
    response.delete_cookie('user_id')
    try:
        Session.objects.filter(session_id=session_id).delete()
    except Session.DoesNotExist:
        pass
    return response


def main(request):
    error = ""
    form = ElementSelectForm()
    if request.method == 'POST':
        form = ElementSelectForm(request.POST)
        if form.is_valid():
            return redirect('get', element_name = form.cleaned_data['element_name'])
        else:
            error = "Некорректно заполнена форма"
    data = {
        'form': form,
        'error': error
    }
    return render(request,'account/main.html', data)


def profile(request):
    user_id = request.COOKIES.get('user_id')
    error = ""
    user = User.objects.get(pk=user_id)
    form = UserUpdateForm(initial={
        'user_name': user.user_name,
        'user_email': user.user_email,
    })
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            password = form.cleaned_data['user_password']
            password_confirm = form.cleaned_data['password_confirm']
            if password == password_confirm:
                form.save(commit=False)
                user.user_password = (make_password(form.cleaned_data['user_password']))
                user.user_email = form.cleaned_data['user_email']
                user.user_name = form.cleaned_data['user_name']
                user.save()
                return redirect('profile')
            else:
                error = "Пароли не совпадают"
        else:
            error = "Введены некорректные данные"

    data = {
        'form': form,
        'error': error
    }
    return render(request,'account/profile.html', data)

def get(request, element_name):
    user_id = request.COOKIES.get('user_id')
    element = Element.objects.get(element_name=element_name)
    user = User.objects.get(pk=user_id)
    permission = Permission.objects.get(role_id=user.role_id, element_id=element.pk)
    read_permission = permission.read_permission
    create_permission = permission.create_permission
    update_permission = permission.update_permission
    delete_permission = permission.delete_permission
    if read_permission or create_permission or update_permission or delete_permission:
        data = {
            'element_name': element_name,
            'read_permission': read_permission,
            'create_permission': create_permission,
            'update_permission': update_permission,
            'delete_permission': delete_permission
        }
        return render(request,'account/get.html', data)
    else:
        return HttpResponse("<h1>Нет прав доступа к запрашиваемому ресурсу.<br>403 Forbidden</h1>")
