from django import forms
from django.core.validators import RegexValidator

class AdminLoginForm(forms.Form):
    phone_number = forms.CharField(
        max_length=15,
        validators=[RegexValidator(
            regex=r'^8-\d{3}-\d{3}-\d{4}$',
            message='Phone number must be in the format: 8-xxx-xxx-xxxx',
        )],
        widget=forms.TextInput(attrs={'placeholder': '8-xxx-xxx-xxxx', 'id': 'phone'}),
        label="Телефон"
    )
    password = forms.CharField(
        max_length=10,
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль...', 'id': 'password', 'pattern': '(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}'}))

class AromatAddForm(forms.Form):
    code = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'Код...', 'id': 'code', 'min': 100}),
        label="Код")
    aromatname = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Название...', 'id': 'aromatname'}),
        label="Название аромата")
    size = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'Объем...', 'id': 'size', 'min': 0}),
        label="Объем")
    cost = forms.DecimalField(
        widget=forms.NumberInput(attrs={'placeholder': 'Цена...', 'id': 'cost', 'min': 0}),
        label="Цена",
        max_digits=10, decimal_places=2) # Пример для максимального количества цифр и десятичных знаков

class SellerRegisterForm(forms.Form):
    lastname = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Фамилия...', 'id': 'lastname'}),
        label="Фамилия")
    firstname = forms.CharField( 
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Имя...', 'id': 'firstname'}),
        label="Имя")
    phone_number = forms.CharField(
        max_length=15,
        validators=[RegexValidator(
            regex=r'^8-\d{3}-\d{3}-\d{4}$',
            message='Phone number must be in the format: 8-xxx-xxx-xxxx',
        )],
        widget=forms.TextInput(attrs={'placeholder': '8-xxx-xxx-xxxx', 'id': 'phone'}),
        label="Телефон"
    )
    password = forms.CharField(
        max_length=10,
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль...', 'id': 'password', 'pattern': '(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}'}),
        label="Пароль")
