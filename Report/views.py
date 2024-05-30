from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AdminLoginForm, AromatAddForm, SellerRegisterForm
from .models import Administrator, Aromat, Seller
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password

# Create your views here.

def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            print("Phone: ", phone_number, "password: ", password)

            try:
                admin = Administrator.objects.get(phone_number=phone_number)
                print("Admin: ", admin)
                print(admin.check_password(password))
                if admin.check_password(password):
                    # Логика для входа (например, установка сессии или редирект)
                    request.session['admin_id'] = admin.id  # Пример установки сессии
                    print("Все успешно")
                    return redirect('aromat_add')  # Переход на страницу админ панели
                else:
                    messages.error(request, 'Неверный номер телефона или пароль!')
            except Administrator.DoesNotExist:
                messages.error(request, 'Неверный номер телефона или пароль!')
    else:
        form = AdminLoginForm()
    return render(request, 'report/admin_login.html', {'form': form})

def aromat_add(request):
    message = None
    admin_name = ""
    admin_id = request.session.get('admin_id')
    if admin_id:
        try:
            admin = Administrator.objects.get(id=admin_id)
            # Теперь у вас есть объект admin с данными администратора
            admin_name = f"{admin.last_name} {admin.first_name}"
        except Administrator.DoesNotExist:
            admin = None
    else:
        admin = None

    if request.method == 'POST':
        form = AromatAddForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            aromatname = form.cleaned_data['aromatname']
            size = form.cleaned_data['size']
            cost = form.cleaned_data['cost']
            
            if Aromat.objects.filter(code=code).exists():
                message = 'Аромат с таким кодом уже существует.'
            elif Aromat.objects.filter(name=aromatname).exists():
                message = 'Аромат с таким названием уже существует.'
            elif size <= 0 or cost <= 0:
                message = 'Объем и цена должны быть положительными числами.'
            else:
                new_aromat = Aromat(code=code, name=aromatname, volume=size, price=cost)
                new_aromat.save()
                message = 'Аромат успешно добавлен.'
    else:
        form = AromatAddForm()
    
    return render(request, 'report/aromat_add.html', {'form': form, 'message': message, 'admin_name': admin_name})

def aromat_list(request):
    admin_name = ""
    admin_id = request.session.get('admin_id')
    if admin_id:
        try:
            admin = Administrator.objects.get(id=admin_id)
            # Теперь у вас есть объект admin с данными администратора
            admin_name = f"{admin.last_name} {admin.first_name}"
        except Administrator.DoesNotExist:
            admin = None
    else:
        admin = None

    aromat_objects = Aromat.objects.all()

    return render(request, 'report/aromat_list.html', {'aromat_objects': aromat_objects, 'admin_name': admin_name})


def seller_register(request):
    message = None
    admin_name = ""
    admin_id = request.session.get('admin_id')
    if admin_id:
        try:
            admin = Administrator.objects.get(id=admin_id)
            # Теперь у вас есть объект admin с данными администратора
            admin_name = f"{admin.last_name} {admin.first_name}"
        except Administrator.DoesNotExist:
            admin = None
    else:
        admin = None

    if request.method == 'POST':
        form = SellerRegisterForm(request.POST)
        if form.is_valid():
            lastname = form.cleaned_data['lastname']
            firstname = form.cleaned_data['firstname']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            
            # Проверяем, что продавец с таким номером телефона не существует
            if Seller.objects.filter(phone_number=phone_number).exists():
                message = 'Продавец с таким номером телефона уже существует.'
            # Проверяем, что пароль соответствует требованиям
            # elif not (any(c.isalpha() for c in password) and any(c.isdigit() for c in password)):
            #     message = 'Пароль должен содержать хотя бы одну латинскую букву и одну цифру.'
            else:
                # Создаем хэш пароля
                hashed_password = make_password(password)
                # Создаем нового продавца
                new_seller = Seller(lastname=lastname, firstname=firstname, phone_number=phone_number, password=hashed_password)
                new_seller.save()
                message = 'Продавец успешно добавлен.'
    else:
        form = SellerRegisterForm()
    return render(request, 'report/seller_register.html', {'form': form, 'message': message, 'admin_name': admin_name})

def seller_report(request):
    admin_name = ""
    admin_id = request.session.get('admin_id')
    if admin_id:
        try:
            admin = Administrator.objects.get(id=admin_id)
            # Теперь у вас есть объект admin с данными администратора
            admin_name = f"{admin.last_name} {admin.first_name}"
        except Administrator.DoesNotExist:
            admin = None
    else:
        admin = None

    seller_objects = Seller.objects.all()

    return render(request, 'report/seller_report.html', {"seller_objects": seller_objects, "admin_name": admin_name})

def logout_view(request):
    logout(request)
    # После выхода перенаправляем пользователя на страницу входа
    return redirect('admin_login')