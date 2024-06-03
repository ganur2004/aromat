from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SellerLoginForm, AromatSoldForm
#from Aromat.report.models import Seller
from report.models import Seller, Aromat, SoldAromat
from django.contrib.auth import logout
from django.utils import timezone

# Create your views here.

def seller_login(request):
    if request.method == 'POST':
        form = SellerLoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            print("Phone: ", phone_number, "password: ", password)

            try:
                seller = Seller.objects.get(phone_number=phone_number)
                print("Seller: ", seller)
                print(seller.check_password(password))
                if seller.check_password(password):
                    # Логика для входа (например, установка сессии или редирект)
                    request.session['seller_id'] = seller.id  # Пример установки сессии
                    print("Все успешно")
                    return redirect('aromat_sold_list')  # Переход на страницу админ панели
                else:
                    messages.error(request, 'Неверный номер телефона или пароль!')
            except Seller.DoesNotExist:
                messages.error(request, 'Неверный номер телефона или пароль!')
    else:
        form = SellerLoginForm()
    return render(request, 'seller/seller_login.html', {'form': form})

def aromat_sold(request):
    seller_name = ""
    message = None
    seller_id = request.session.get('seller_id')
    if seller_id:
        try:
            seller = Seller.objects.get(id=seller_id)
            seller_name = f"{seller.lastname} {seller.firstname}"
        except Seller.DoesNotExist:
            seller = None
    else:
        seller = None

    if request.method == 'POST':
        form = AromatSoldForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            aromat = Aromat.objects.get(code=code)
            name = form.cleaned_data['name']
            volume = aromat.volume
            size = form.cleaned_data['size']
            paymenttype = form.cleaned_data['paymenttype']
            price = form.cleaned_data['cost']
            date = timezone.now()  # Устанавливаем сегодняшнюю дату
            sellername = seller_name

            if volume >= size:
                volume = aromat.volume - form.cleaned_data['size']
                aromat.volume = volume
                aromat.save()
                new_sold_aromat = SoldAromat(seller_id=seller_id, code=code, name=name, volume=volume, masla=size, paymenttype=paymenttype, price=price, date=date, sellername=sellername)
                new_sold_aromat.save()
                message = 'Продажа успешно сохранена!'
            else:
                message = "Обьем этого аромата не хватает!"


    else:
        form = AromatSoldForm()
        initial_data = {'date': timezone.now().date(), 'sellername': seller_name}
        form = AromatSoldForm(initial=initial_data)  # Передача начальных данных в форму
    aromats = Aromat.objects.all()

    return render(request, 'seller/aromat_sold.html', {"form": form, 'aromats': aromats, "seller_name": seller_name, 'message': message})

def aromat_sold_list(request):
    seller_name = ""
    message = None
    seller_id = request.session.get('seller_id')
    if seller_id:
        try:
            seller = Seller.objects.get(id=seller_id)
            seller_name = f"{seller.lastname} {seller.firstname}"
        except Seller.DoesNotExist:
            seller = None
    else:
        seller = None

    aromat_sold_list = SoldAromat.objects.filter(seller_id=seller_id)

    return render(request, "seller/aromat_sold_list.html", {"seller_name": seller_name, "aromat_sold_list": aromat_sold_list})

def seller_logout(request):
    logout(request)
    # После выхода перенаправляем пользователя на страницу входа
    return redirect('seller_login')