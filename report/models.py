from django.db import models

# Create your models here.

from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password, check_password

class Administrator(models.Model):
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(
            regex=r'^8-\d{3}-\d{3}-\d{4}$',
            message='Phone number must be in the format: 8-xxx-xxx-xxxx',
            code='invalid_phone_number'
        )],
        verbose_name='Телефон'
    )
    password = models.CharField(max_length=50, verbose_name='Пароль')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    class Meta:
        verbose_name = 'Администратор'
        verbose_name_plural = 'Администраторы'
    
class Branch(models.Model):
    cityname = models.CharField(max_length=100, verbose_name="Название города")

    class Meta:
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы'

    def __str__(self):
        return self.cityname

class Aromat(models.Model):
    code = models.CharField(max_length=5, verbose_name='Код')
    name = models.CharField(max_length=255, verbose_name='Название')
    volume = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Объем')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name='Филиал')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Аромат'
        verbose_name_plural = 'Ароматы'

class Seller(models.Model):
    lastname= models.CharField(max_length=50,  verbose_name='Фамилия')
    firstname = models.CharField(max_length=50, verbose_name='Имя')
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(
            regex=r'^8-\d{3}-\d{3}-\d{4}$',
            message='Phone number must be in the format: 8-xxx-xxx-xxxx',
            code='invalid_phone_number'
        )],
        verbose_name='Телефон'
    )
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name='Филиал')
    password = models.CharField(max_length=50, verbose_name='Пароль')

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    class Meta:
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'

class SoldAromat(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=5, verbose_name='Код')
    name = models.CharField(max_length=100, verbose_name='Название аромата')
    volume = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Объем', default=0)
    masla = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Масла', default=0)
    paymenttype = models.CharField(max_length=50, verbose_name='Тип оплаты')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Касса', default=0)
    date = models.DateTimeField(verbose_name='Дата')
    sellername = models.CharField(max_length=255, verbose_name='Имя продавца')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name='Филиал')
    coment = models.CharField(null=True, verbose_name="Комментарий", max_length=5000)

    class Meta:
        verbose_name = 'Проданные ароматы'
        verbose_name_plural = 'Проданные ароматы'

    def __str__(self):
        return f"{self.code} - {self.sellername} - {self.date}"
    
