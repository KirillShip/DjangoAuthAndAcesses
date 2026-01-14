from django.http import HttpResponse
from django.shortcuts import render
from account.models import Role, Element, Permission, User
from .forms import *

def admin(request):
    user_id = request.COOKIES.get('user_id')
    user = User.objects.get(pk=user_id)
    if user.role_id.pk != 1:
        return HttpResponse("<h1>Нет прав доступа к запрашиваемому ресурсу.<br>403 Forbidden</h1>")
    error = ""
    element_form = ElementSelectForm(request.POST)
    role_form = RoleSelectForm(request.POST)
    permission_form = UserPermissionForm(request.POST)
    if request.method == 'POST':
        if element_form.is_valid() and role_form.is_valid() and permission_form.is_valid():
            try:
                role_id = Role.objects.get(role_name=role_form.cleaned_data['role_name'])
                element_id = Element.objects.get(element_name=element_form.cleaned_data['element_name'])
                try:
                    permission_exist = Permission.objects.get(role_id=role_id, element_id=element_id)
                    permission = Permission(
                        pk=permission_exist.pk,
                        role_id=role_id,
                        element_id=element_id,
                        create_permission=permission_form.cleaned_data['create_permission'],
                        update_permission=permission_form.cleaned_data['update_permission'],
                        delete_permission=permission_form.cleaned_data['delete_permission'],
                        read_permission=permission_form.cleaned_data['read_permission'],
                    )
                    permission.save()
                except Permission.DoesNotExist:
                    permission = Permission(
                        role_id = role_id,
                        element_id = element_id,
                        create_permission = permission_form.cleaned_data['create_permission'],
                        update_permission = permission_form.cleaned_data['update_permission'],
                        delete_permission = permission_form.cleaned_data['delete_permission'],
                        read_permission = permission_form.cleaned_data['read_permission'],
                    )
                    permission.save()
            except Role.DoesNotExist or Element.DoesNotExist or Permission.DoesNotExist:
                error = "Не найдена запись в БД"
        else:
            error = "Некорректное заполнение формы"

    data = {
        'element_form': element_form,
        'role_form': role_form,
        'permission_form': permission_form,
        'error': error,
    }
    return render(request, 'admin/admin.html', data)
