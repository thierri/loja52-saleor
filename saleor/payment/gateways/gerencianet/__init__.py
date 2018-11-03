import uuid
from decimal import Decimal
from typing import Dict

from django.conf import settings
from prices import Money

from ... import TransactionKind
from ...models import Payment
from ...utils import create_transaction
from .forms import CreditCardPaymentForm
from .gncharge import GNCharge
from gerencianet import Gerencianet


def dummy_success():
    return True

def get_client_token(**connection_params):   
    return str(uuid.uuid4())


def get_form_class():
    return CreditCardPaymentForm


def authorize(payment: Payment, gerencianet_data: str, **connection_params):
    _GNCharge = GNCharge(payment.order, **connection_params)
    error = None

    try:
        gn_response = _GNCharge.create_charge()
    except expression as identifier:
        error = 'Unable to create charge on Gerencianet'
        
    txn = create_transaction(
        payment=payment,
        kind=TransactionKind.AUTH,
        amount=payment.total,
        currency=payment.currency,
        gateway_response=gn_response,
        token=gerencianet_data,
        is_success=(error is None))
    return txn, error


def void(payment: Payment, **connection_params: Dict):
    error = None
    success = dummy_success()
    if not success:
        error = 'Unable to void the transaction.'
    txn = create_transaction(
        payment=payment,
        kind=TransactionKind.VOID,
        amount=payment.total,
        currency=payment.currency,
        gateway_response={},
        token=str(uuid.uuid4()),
        is_success=success)
    return txn, error


def capture(payment: Payment, amount: Decimal, **connection_params):
    _GNCharge = GNCharge(payment.order, **connection_params)
    error = None

    auth_transaction = payment.transactions.filter(
        kind=TransactionKind.AUTH, is_success=True).first()

    payment_data = {
        'charge_id': auth_transaction.gateway_response['data']['charge_id'],
        'card_token': auth_transaction.token
    }
    try:
        gn_response = _GNCharge.pay_charge(**payment_data)
    except expression as identifier:
        error = 'Unable to create charge on Gerencianet'

    txn = create_transaction(
        payment=payment,
        kind=TransactionKind.CAPTURE,
        amount=amount,
        currency=payment.currency,
        token=str(uuid.uuid4()),
        is_success=success)
    return txn, error


def refund(payment: Payment, amount: Decimal):
    error = None
    success = dummy_success()
    if not success:
        error = 'Unable to process refund'
    txn = create_transaction(
        payment=payment,
        kind=TransactionKind.REFUND,
        amount=amount,
        currency=payment.currency,
        token=str(uuid.uuid4()),
        is_success=success)
    return txn, error
