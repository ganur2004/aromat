from django.db import models

# Create your models here.

from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password, check_password

class Administrator(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(
            regex=r'^8-\d{3}-\d{3}-\d{4}$',
            message='Phone number must be in the format: 8-xxx-xxx-xxxx',
            code='invalid_phone_number'
        )]
    )
    password = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    class Meta:
        verbose_name = 'Администратор'
        verbose_name_plural = 'Администраторы'
    

class Aromat(models.Model):
    code = models.CharField(max_length=3, unique=True, verbose_name='Код')
    name = models.CharField(max_length=255, unique=True, verbose_name='Название')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    volume = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Объем')

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
        )]
    )
    password = models.CharField(max_length=20)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    class Meta:
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'

    