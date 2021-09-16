from django.forms import ModelForm
from django import forms
import datetime
from .models import Credicard
import re
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class PaymentForm(ModelForm):
    class Meta:
        model =  Credicard
        fields = ['name', 'card_number', 'card_expiration', 'cvv']
        #fields -> como y que campos de entrada mostrar en el FORMULARIO template
        widgets = {
            "card_number" : forms.TextInput(
                attrs = {
                    "placeholder": "Credicard without space",
                    "style" : "border-radius: 10px"
                }
            )
        }

    amount = forms.DecimalField(required = True, max_value = 99999999999999999)

    def clean_cvv(self):
        cvv =  self.cleaned_data['cvv']
        if not re.match(r"\d\d\d|\d\d\d\d" , cvv):
            raise ValidationError(_("CVV must be number with 3 to 4 digits"))
            #Muestra el mensaje de error en el HTML
        return cvv

    def clean_card_expiration(self):
        exp = self.cleaned_data['card_expiration']
        if not re.match(r"\d\d/\d\d", exp):
            raise ValidationError(_("Invalid Expiration format, you must set it in AA/MM"))
        return exp
    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise ValidationError(_("Amount must be more than 0 and have equal or less 17 digits"))
        return amount
    def clean_card_number(self):
        number = self.cleaned_data['card_number']
        if re.findall(r"[^0-9]+", number) != []:
            raise ValidationError(_("Credicard must have numbers only."))
        return number
