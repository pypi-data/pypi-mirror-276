from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

from .models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите имя пользователя'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите пароль'
    }))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите имя'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите имя пользователя'
    }))
    number = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Подтвердите пароль'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите адрес эл. почты'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите пароль'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Подтвердите пароль'
    }))

    class Meta:
        model = User
        fields = ('first_name', 'username', 'number', 'email', 'password1', 'password2')


# class OrderForm(forms.ModelForm):
#     number_car = forms.CharField(widget=forms.TextInput(attrs={
#         'class': 'form-control', 'placeholder': 'Гос. номер авто'
#     }))
#     description = forms.CharField(widget=forms.TextInput(attrs={
#         'class': 'form-control', 'placeholder': 'Описание'
#     }))
#
#     class Meta:
#         model = Order
#         fields = ('number_car', 'description')

