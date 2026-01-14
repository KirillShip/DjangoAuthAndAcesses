from django import forms
from account.models import Role, Permission, Element

class RoleSelectForm(forms.ModelForm):
    role_name = forms.ModelChoiceField(
        queryset=Role.objects.all().values_list('role_name', flat=True),
        empty_label="Выберите роль",
        widget=forms.Select(attrs={'class': 'form-control'}),
        to_field_name='role_name'
    )
    class Meta:
        model = Role
        fields = ('role_name',)


class ElementSelectForm(forms.ModelForm):
    element_name = forms.ModelChoiceField(
        queryset=Element.objects.all().values_list('element_name', flat=True),
        empty_label="Выберите элемент",
        widget=forms.Select(attrs={'class': 'form-control'}),
        to_field_name='element_name'
    )
    class Meta:
        model = Element
        fields = ('element_name',)


class UserPermissionForm(forms.ModelForm):
    create_permission = forms.BooleanField(required=False, label = "Разрешение на создание")
    update_permission = forms.BooleanField(required=False, label="Разрешение на обновление")
    delete_permission = forms.BooleanField(required=False, label="Разрешение на удаление")
    read_permission = forms.BooleanField(required=False, label="Разрешение на чтение")
    class Meta:
        model = Permission
        fields = ('create_permission', 'update_permission', 'delete_permission', 'read_permission')