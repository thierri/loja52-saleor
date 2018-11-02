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
        # Dummy provider requires no real token
        teste = GNCharge(self.payment.order, **self.gateway_params).get_cleaned_products()

        order_lines = self.payment.order.lines.all()
        fake_token = self.gateway.get_charge_id(order_lines, **self.gateway_params)
        # fake_token = 'oi'
      
        self.payment.authorize(fake_token)
        charge_status = self.cleaned_data['charge_status']
        if charge_status == ChargeStatus.NOT_CHARGED:
            return
        self.payment.capture()
        if charge_status == ChargeStatus.FULLY_REFUNDED:
            self.payment.refund()
        return self.payment
