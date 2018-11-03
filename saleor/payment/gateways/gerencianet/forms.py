from django import forms
from django.utils.translation import pgettext_lazy
from ... import ChargeStatus
from ...forms import PaymentForm
from .gncharge import GNCharge

# Override Template Name to a custon one, without 'Name' param
class JSOnlyCharField(forms.CharField):
    def __init__(self, **kwargs):
        super().__init__(required=False,**kwargs)
        self.widget.template_name = 'django/forms/widgets/input_js_only.html'


class CreditCardPaymentForm(PaymentForm):
    charge_status = forms.ChoiceField(
        label=pgettext_lazy('Payment status form field', 'Payment status'),
        choices=ChargeStatus.CHOICES, initial=ChargeStatus.NOT_CHARGED,
        widget=forms.RadioSelect)
    
    credit_card_brand = JSOnlyCharField(
        label=pgettext_lazy('Brand of your credit card', 'Credit Card Brand')
    )
    credit_card_number = JSOnlyCharField(
        label=pgettext_lazy('Payment status form field', 'Credit Card Number')
    )
    credit_card_cvv = JSOnlyCharField(
        label=pgettext_lazy('Payment status form field', 'Credit Card CVV')
    )
    credit_card_expiration_month = JSOnlyCharField(
        label=pgettext_lazy('Payment status form field', 'Expiration Month')
    )
    credit_card_expiration_year = JSOnlyCharField(
        label=pgettext_lazy('Payment status form field', 'Expiration Year')
    )
    credit_card_token = forms.CharField(widget=forms.HiddenInput())


    def process_payment(self):
        
        self.payment.authorize(self.cleaned_data['credit_card_token'])
        capture = self.payment.capture()
    
        return self.payment
