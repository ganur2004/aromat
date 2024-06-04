from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import AdminLoginForm, AromatAddForm, SellerRegisterForm, FilterForm, AromatForm
from .models import Administrator, Aromat, Seller, SoldAromat
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.db.models import Sum
from datetime import date as dt_date, timedelta
from django.db.models.functions import TruncDate
from django.contrib import messages

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
                    request.session['admin_id'] = admin.id  
                    print("Все успешно")
                    return redirect('aromat_sold_list_admin')
                else:
                    messages.error(request, 'Неверный номер телефона или пароль!')
            except Administrator.DoesNotExist:
                messages.error(request, 'Неверный номер телефона или пароль!')
    else:
        form = AdminLoginForm()
    return render(request, 'report/admin_login.html', {'form': form})

def admin_session(request):
    admin_name = ""
    admin_id = request.session.get('admin_id')
    print("Admin id", admin_id)
    if admin_id:
        try:
            admin = Administrator.objects.get(id=admin_id)
            admin_name = f"{admin.last_name} {admin.first_name}"
        except Administrator.DoesNotExist:
            admin = None
    else:
        admin = None
    return admin_name


def aromat_add(request):
    message = None
    admin_name = admin_session(request)
    admin_id = request.session.get('admin_id')

    if admin_id:
        if request.method == 'POST':
            form = AromatAddForm(request.POST)
            if form.is_valid():
                code = form.cleaned_data['code']
                aromatname = form.cleaned_data['aromatname']
                size = form.cleaned_data['size']
                
                if Aromat.objects.filter(code=code).exists():
                    message = 'Аромат с таким кодом уже существует.'
                elif Aromat.objects.filter(name=aromatname).exists():
                    message = 'Аромат с таким названием уже существует.'
                elif size <= 0:
                    message = 'Объем должен быть положительными числами.'
                else:
                    new_aromat = Aromat(code=code, name=aromatname, volume=size)
                    new_aromat.save()
                    message = 'Аромат успешно добавлен.'
        else:
            form = AromatAddForm()
        
        return render(request, 'report/aromat_add.html', {'form': form, 'message': message, 'admin_name': admin_name})
    else:
        return redirect('admin_login')

def aromat_list(request):
    admin_name = admin_session(request)
    admin_id = request.session.get('admin_id')
    
    if admin_id:
        code = request.GET.get('code')
        aromatname = request.GET.get('aromatname')
        aromat_objects = Aromat.objects.all()
        
        if code:
            aromat_objects = aromat_objects.filter(code=code)
        if aromatname:
            aromat_objects = aromat_objects.filter(name__icontains=aromatname)

        codes = Aromat.objects.values_list('code', flat=True).distinct()
        names = Aromat.objects.values_list('name', flat=True).distinct()
        context = {
            'admin_name': admin_name,
            'aromat_objects': aromat_objects,
            'codes': codes,
            'names': names
        }

        aromat_objects = Aromat.objects.all()

        return render(request, 'report/aromat_list.html', context)
    else:
        return redirect('admin_login')


def seller_register(request):
    message = None
    admin_name = admin_session(request)
    admin_id = request.session.get('admin_id')

    if admin_id:
        if request.method == 'POST':
            form = SellerRegisterForm(request.POST)
            if form.is_valid():
                lastname = form.cleaned_data['lastname']
                firstname = form.cleaned_data['firstname']
                phone_number = form.cleaned_data['phone_number']
                password = form.cleaned_data['password']
                
                if Seller.objects.filter(phone_number=phone_number).exists():
                    messages.error(request, 'Продавец с таким номером телефона уже существует.')
                else:
                    hashed_password = make_password(password)
                    new_seller = Seller(lastname=lastname, firstname=firstname, phone_number=phone_number, password=hashed_password)
                    new_seller.save()
                    messages.success(request, 'Продавец успешно добавлен.')
        else:
            form = SellerRegisterForm()
        return render(request, 'report/seller_register.html', {'form': form, 'admin_name': admin_name})
    else:
        return redirect('admin_login')


def seller_report(request):
    admin_name = admin_session(request)
    admin_id = request.session.get('admin_id')
    
    if admin_id:
        today = dt_date.today().strftime('%Y-%m-%d')
        
        date = request.GET.get('date') or today
        date_range = request.GET.get('date_range', 'all')

        if date_range == '7_days':
            start_date = dt_date.today() - timedelta(days=7)
        elif date_range == '1_month':
            start_date = dt_date.today() - timedelta(days=30)
        elif date_range == '3_months':
            start_date = dt_date.today() - timedelta(days=90)
        elif date_range == '6_months':
            start_date = dt_date.today() - timedelta(days=180)
        elif date_range == '9_months':
            start_date = dt_date.today() - timedelta(days=270)
        elif date_range == '1_year':
            start_date = dt_date.today() - timedelta(days=365)
        else:
            start_date = None

        seller_objects = Seller.objects.all()
        total_all_price = 0

        seller_prices = []
        for seller in seller_objects:
            if start_date:
                total_price = SoldAromat.objects.filter(seller=seller, date__date__range=[start_date, dt_date.today()]).aggregate(total_price=Sum('price'))['total_price']
            else:
                total_price = SoldAromat.objects.filter(seller=seller, date__date=date).aggregate(total_price=Sum('price'))['total_price']
            
            if total_price is None:
                total_price = 0
            total_all_price += total_price
            seller_prices.append({'seller': seller, 'total_price': total_price or 0})

            context = {
            "seller_prices": seller_prices,
            "admin_name": admin_name,
            "selected_date": date,
            "selected_date_range": date_range,
            "total_all_price": total_all_price,
            "date_range_options": [
                ('all', 'Все время'),
                ('7_days', 'Последние 7 дней'),
                ('1_month', 'Последний месяц'),
                ('3_months', 'Последние 3 месяца'),
                ('6_months', 'Последние 6 месяцев'),
                ('9_months', 'Последние 9 месяцев'),
                ('1_year', 'Последний год'),
            ]
        }

        return render(request, 'report/seller_report.html', context)
    else:
        return redirect('admin_login')


def edit_aromat(request, pk):
    message = None
    aromat = get_object_or_404(Aromat, pk=pk)
    admin_name = admin_session(request)
    admin_id = request.session.get('admin_id')

    if admin_id:
        if request.method == "POST":
            form = AromatForm(request.POST, instance=aromat)
            if form.is_valid():
                form.save()
                return redirect('aromat_list')
        else:
            form = AromatForm(instance=aromat)
        return render(request, 'report/edit_aromat.html', {'form': form, 'message': message, "admin_name": admin_name})
    else:
        return redirect('admin_login')


def delete_aromat(request, pk):
    admin_name = admin_session(request)
    admin_id = request.session.get('admin_id')

    if admin_id:
        aromat = get_object_or_404(Aromat, pk=pk)
        if request.method == "POST":
            aromat.delete()
            return redirect('aromat_list')
        return render(request, 'report/confirm_delete.html', {'aromat': aromat, "admin_name": admin_name})
    else:
        return redirect('admin_login')


def aromat_sold_list_admin(request):
    admin_name = admin_session(request)
    admin_id = request.session.get('admin_id')
    
    if admin_id:
        code = request.GET.get('code')
        paymenttype = request.GET.get('paymenttype')
        date = request.GET.get('date')

        today = dt_date.today().strftime('%Y-%m-%d')

        aromat_sold_objects = SoldAromat.objects.all()

        if code:
            aromat_sold_objects = aromat_sold_objects.filter(code=code)
        if paymenttype:
            aromat_sold_objects = aromat_sold_objects.filter(paymenttype=paymenttype)
        if date:
            aromat_sold_objects = aromat_sold_objects.filter(date__date=date)
        else:
            date = today

        total_price = aromat_sold_objects.aggregate(Sum('price'))['price__sum'] or 0

        codes = SoldAromat.objects.values_list('code', flat=True).distinct()
        paymenttypes = SoldAromat.objects.values_list('paymenttype', flat=True).distinct()
        dates = SoldAromat.objects.values_list('date', flat=True).distinct()

        dates = [d.strftime('%Y-%m-%d') for d in dates]

        context = {
            'admin_name': admin_name,
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

        return render(request, 'report/aromat_sold_list_admin.html', context)
    else:
        return redirect('admin_login')


def seller_report_page(request, pk):
    admin_name = admin_session(request)
    admin_id = request.session.get('admin_id')
    
    if admin_id:
        seller = get_object_or_404(Seller, pk=pk)
        firstname = seller.firstname
        lastname = seller.lastname
        phone = seller.phone_number
        seller_name = f"{lastname} {firstname}"

        try:
            seller = Seller.objects.get(id=pk)
        except Seller.DoesNotExist:
            return render(request, 'report/seller_report.html', {"admin_name": admin_name, "error": "Продавец не найден"})

        sales_by_date = (
            SoldAromat.objects.filter(seller=seller)
            .annotate(date_only=TruncDate('date'))
            .values('date_only')
            .annotate(total_price=Sum('price'))
            .order_by('date_only')
        )

        total_price = SoldAromat.objects.filter(seller=seller).aggregate(total_price=Sum('price'))['total_price']
        if total_price is None:
                total_price = 0


        context = {
            "admin_name": admin_name,
            "seller_name": seller_name,
            "seller_phone": phone,
            "sales_by_date": sales_by_date,
            "total_price": total_price
        }
        return render(request, 'report/seller_report_page.html', context)
    else:
        return redirect('admin_login')


def logout_view(request):
    logout(request)
    return redirect('admin_login')