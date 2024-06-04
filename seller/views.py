from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SellerLoginForm, AromatSoldForm
from report.models import Seller, Aromat, SoldAromat
from django.contrib.auth import logout
from django.utils import timezone
from datetime import date as dt_date
from django.db.models import Sum

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
                    request.session['seller_id'] = seller.id  
                    print("Все успешно")
                    return redirect('aromat_sold_list')
                else:
                    messages.error(request, 'Неверный номер телефона или пароль!')
            except Seller.DoesNotExist:
                messages.error(request, 'Неверный номер телефона или пароль!')
    else:
        form = SellerLoginForm()
    return render(request, 'seller/seller_login.html', {'form': form})


def seller_session(request):
    seller_id = request.session.get('seller_id')
    seller_name = ""
    if seller_id:
        try:
            seller = Seller.objects.get(id=seller_id)
            seller_name = f"{seller.lastname} {seller.firstname}"
        except Seller.DoesNotExist:
            seller = None
    else:
        seller = None
    return seller_name


def aromat_sold(request):
    seller_name = seller_session(request)
    seller_id = request.session.get('seller_id')
    message = None
    if seller_id:
        if request.method == 'POST':
            form = AromatSoldForm(request.POST)
            if form.is_valid():
                code = form.cleaned_data['code']
                aromat = Aromat.objects.get(code=code)
                name = form.cleaned_data['name']
                size = form.cleaned_data['size']
                paymenttype = form.cleaned_data['paymenttype']
                price = form.cleaned_data['cost']
                date = timezone.now()
                sellername = seller_name

                if aromat.volume >= size:
                    volume = aromat.volume - size
                    aromat.volume = volume
                    aromat.save()
                    new_sold_aromat = SoldAromat.objects.create(seller_id=seller_id, code=code, name=name, volume=volume, masla=size, paymenttype=paymenttype, price=price, date=date, sellername=sellername)
                    message = 'Продажа успешно сохранена!'
                else:
                    message = "Недостаточное количество товара!"
        else:
            form = AromatSoldForm(initial={'date': timezone.now().date(), 'sellername': seller_name})

        aromats = Aromat.objects.all()
        return render(request, 'seller/aromat_sold.html', {"form": form, 'aromats': aromats, "seller_name": seller_name, 'message': message})
    else:
        return redirect('seller_login')
        


def aromat_sold_list(request):
    seller_name = seller_session(request)
    message = None
    seller_id = request.session.get('seller_id')
    if seller_id:
        code = request.GET.get('code')
        paymenttype = request.GET.get('paymenttype')
        date = request.GET.get('date')
        today = dt_date.today().strftime('%Y-%m-%d')
        aromat_sold_objects = SoldAromat.objects.filter(seller_id=seller_id)

        if code:
            aromat_sold_objects = aromat_sold_objects.filter(code=code)
        if paymenttype:
            aromat_sold_objects = aromat_sold_objects.filter(paymenttype=paymenttype)
        if date:
            aromat_sold_objects = aromat_sold_objects.filter(date__date=date)
        else:
            date = today
            aromat_sold_objects = aromat_sold_objects.filter(date__date=today)

        total_price = aromat_sold_objects.aggregate(Sum('price'))['price__sum'] or 0
        codes = SoldAromat.objects.values_list('code', flat=True).distinct()
        paymenttypes = SoldAromat.objects.values_list('paymenttype', flat=True).distinct()
        dates = SoldAromat.objects.values_list('date', flat=True).distinct()
        dates = [d.strftime('%Y-%m-%d') for d in dates]
        context = {
            'seller_name': seller_name,
            'aromat_sold_objects': aromat_sold_objects.order_by('-id'),
            'codes': codes,
            'paymenttypes': paymenttypes,
            'dates': dates,
            'selected_code': code,
            'selected_paymenttype': paymenttype,
            'selected_date': date,
            'total_price': total_price,
            'today': today,
        }

        return render(request, "seller/aromat_sold_list.html", context)
    else:
        return redirect('seller_login')

def seller_logout(request):
    logout(request)
    return redirect('seller_login')