from django import forms
from .models import  User

class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('user_email', 'user_password')
        widgets = {
            "user_email": forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': 'Почта'}
            ),
            "user_password": forms.PasswordInput(
                attrs={'class': 'form-control', 'placeholder': 'Пароль'}
            ),
        }

class UserRegistrationForm(forms.ModelForm):
    password_confirm = forms.CharField(
        widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Подтверждение пароля'}
        ),
        label="Подтверждение пароля"
    )
    class Meta:
        model = User
        fields = ('user_name', 'user_email', 'user_password')
        widgets = {
            "user_name": forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'ФИО'}
            ),
            "user_email": forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': 'Почта'}
            ),
            "user_password": forms.PasswordInput(
                attrs={'class': 'form-control', 'placeholder': 'Пароль'}
            ),
        }

class UserUpdateForm(forms.ModelForm):
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Подтверждение пароля'}
        ),
        label="Подтверждение пароля"
    )
    class Meta:
        model = User
        fields = ('user_name', 'user_email', 'user_password')
        widgets = {
            "user_name": forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'ФИО'}
            ),
            "user_email": forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': 'Почта'}
            ),
            "user_password": forms.PasswordInput(
                attrs={'class': 'form-control', 'placeholder': 'Пароль'}
            ),
        }