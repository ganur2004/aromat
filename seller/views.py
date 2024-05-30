from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SellerLoginForm, AromatSoldForm
#from Aromat.report.models import Seller
from report.models import Seller, Aromat
from django.contrib.auth import logout

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
                    return redirect('aromat_sold')  # Переход на страницу админ панели
                else:
                    messages.error(request, 'Неверный номер телефона или пароль!')
            except Seller.DoesNotExist:
                messages.error(request, 'Неверный номер телефона или пароль!')
    else:
        form = SellerLoginForm()
    return render(request, 'seller/seller_login.html', {'form': form})

def aromat_sold(request):
    seller_name = ""
    seller_id = request.session.get('seller_id')
    if seller_id:
        try:
            seller = Seller.objects.get(id=seller_id)
            # Теперь у вас есть объект admin с данными администратора
            seller_name = f"{seller.lastname} {seller.firstname}"
        except Seller.DoesNotExist:
            admin = None
    else:
        admin = None

    form = AromatSoldForm()

    # if request.method == 'POST':
    #     form = AromatSoldForm(request.POST)
    #     if form.is_valid():
    #         code = form.cleaned_data['code']
    #         size = form.cleaned_data['size']
    #         cost = form.cleaned_data['cost']
    #         paymenttype = form.cleaned_data['paymenttype']
            
    #         if Aromat.objects.filter(code!=code).exists():
    #             message = 'Аромат с таким кодом не существует.'
    #         else:
    #             new_aromat = Aromat(code=code, name=aromatname, volume=size, price=cost)
    #             new_aromat.save()
    #             message = 'Аромат успешно добавлен.'
    # else:
    #     form = AromatAddForm()

    return render(request, 'seller/aromat_sold.html', {"form": form, "seller_name": seller_name})

def seller_logout(request):
    logout(request)
    # После выхода перенаправляем пользователя на страницу входа
    return redirect('seller_login')