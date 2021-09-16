from django.contrib import admin
from .models import Credicard, StatusTrans
from django import forms  # for create a form
from .forms import PaymentForm
from django.shortcuts import render
# Register your models here.

#admin.site.register(Credicard)

@admin.register(Credicard)
class CredicardAdmin(admin.ModelAdmin):
    list_display = ('status', 'name', 'card_number')
    list_filter = ('status',)
    actions = ["fillPaymentForm"]

    @admin.action(description = "Use this for fill form Transbank Transaction")
    def fillPaymentForm(self, request, queryset):
        card = queryset.values()[0]  #it takes one card to fill form Only
        initial = {'name' : card['name'], 'card_number' : card['card_number'], 'card_expiration' : card['card_expiration'], 'cvv' : card['cvv']}
        form = PaymentForm( initial = initial )
        return render(request, 'payment_form.html', context = {'form' : form})

admin.site.register(StatusTrans)
