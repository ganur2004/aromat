from django import forms
from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import Administrator, Aromat, Seller, SoldAromat, Branch


# Administrator
class AdministratorCreationForm(forms.ModelForm):
    class Meta:
        model = Administrator
        fields = ['first_name', 'last_name', 'phone_number', 'password']

    def save(self, commit=True):
        admin = super().save(commit=False)
        admin.password = make_password(self.cleaned_data['password'])
        if commit:
            admin.save()
        return admin

class AdministratorChangeForm(forms.ModelForm):
    class Meta:
        model = Administrator
        fields = ['first_name', 'last_name', 'phone_number', 'password']

    def save(self, commit=True):
        admin = super().save(commit=False)
        if 'password' in self.changed_data:
            admin.password = make_password(self.cleaned_data['password'])
        if commit:
            admin.save()
        return admin

class AdministratorAdmin(admin.ModelAdmin):
    form = AdministratorChangeForm
    add_form = AdministratorCreationForm

    list_display = ('first_name', 'last_name', 'phone_number')
    search_fields = ('first_name', 'last_name', 'phone_number')

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs['form'] = self.add_form
        return super().get_form(request, obj, **kwargs)
    

# Aromat
class AromatAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'volume', 'branch')
    search_fields = ('code', 'name', 'branch')


# Seller
class SellerCreationForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['firstname', 'lastname', 'phone_number', 'password', 'branch']

    def save(self, commit=True):
        seller = super().save(commit=False)
        seller.password = make_password(self.cleaned_data['password'])
        if commit:
            seller.save()
        return seller

class SellerChangeForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['firstname', 'lastname', 'phone_number', 'password', 'branch']

    def save(self, commit=True):
        seller = super().save(commit=False)
        if 'password' in self.changed_data:
            seller.password = make_password(self.cleaned_data['password'])
        if commit:
            seller.save()
        return seller

class SellerAdmin(admin.ModelAdmin):
    form = SellerChangeForm
    add_form = SellerCreationForm

    list_display = ('firstname', 'lastname', 'phone_number', 'branch')
    search_fields = ('firstname', 'lastname', 'phone_number', 'branch')

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs['form'] = self.add_form
        return super().get_form(request, obj, **kwargs)
    
class SoldAromatAdmin(admin.ModelAdmin):
    list_display = ('sellername', 'code', 'name', 'date', 'branch')
    search_fields = ('sellername', 'code', 'name', 'date', 'branch')

admin.site.register(Administrator, AdministratorAdmin)
admin.site.register(Aromat, AromatAdmin)
admin.site.register(Seller, SellerAdmin)
admin.site.register(SoldAromat, SoldAromatAdmin)
admin.site.register(Branch)