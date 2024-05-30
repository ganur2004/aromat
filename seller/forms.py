from django import forms
from django.core.validators import RegexValidator

class SellerLoginForm(forms.Form):
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
    

class AromatSoldForm(forms.Form):
    code = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'Код...', 'id': 'code', 'min': 100}),
        label="Код")
    size = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'Масла...', 'id': 'size', 'min': 0}),
        label="Масла")
    cost = forms.DecimalField(
        widget=forms.NumberInput(attrs={'placeholder': 'Цена...', 'id': 'cost', 'min': 0}),
        label="Цена",
        max_digits=10, decimal_places=2) # Пример для максимального количества цифр и десятичных знаков
    paymenttype = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Тип оплаты...', 'id': 'paymenttype'}),
        label="Тип оплаты")
