from django import forms
from django.core.validators import RegexValidator
from  report.models import SoldAromat, Aromat

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
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль...', 'id': 'password', 'pattern': '(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}'}),
        label="Пароль"
    )
    

class AromatSoldForm(forms.ModelForm):
    PAYMENT_CHOICES = [
        ('Наличные', 'Наличные'),
        ('Карта', 'Карта'),
    ]

    code = forms.ChoiceField(choices=[], label='Код', widget=forms.Select(attrs={'id': 'id_code'}))
    name = forms.ChoiceField(choices=[], label='Название аромата', widget=forms.Select(attrs={'id': 'id_name'}))

    def __init__(self, *args, **kwargs):
        branch = kwargs.pop('branch', None)  # Извлекаем филиал из kwargs
        super(AromatSoldForm, self).__init__(*args, **kwargs)
        if branch:  # Если филиал передан, фильтруем коды и названия ароматов по этому филиалу
            aromats = Aromat.objects.filter(branch=branch)
            self.fields['code'].choices = [(aromat.code, aromat.code) for aromat in aromats]
            self.fields['name'].choices = [(aromat.name, aromat.name) for aromat in aromats]

    size = forms.DecimalField(
        widget=forms.NumberInput(attrs={'placeholder': 'Масла...', 'id': 'size', 'min': 0}),
        label="Масла",
        max_digits=10, decimal_places=2
    )
    cost = forms.DecimalField(
        widget=forms.NumberInput(attrs={'placeholder': 'Цена...', 'id': 'cost', 'min': 0}),
        label="Цена",
        max_digits=10, decimal_places=2
    )
    paymenttype = forms.ChoiceField(
        choices=PAYMENT_CHOICES, 
        label='Тип оплаты',
        widget=forms.Select(attrs={'id': 'id_paymenttype'})
    )

    date = forms.DateField(label='Дата', required=False, widget=forms.DateInput(attrs={'readonly': 'readonly'}))
    sellername = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = SoldAromat
        fields = ['code', 'name', 'size', 'cost', 'paymenttype', 'date', 'sellername']


