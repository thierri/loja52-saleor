from gerencianet import Gerencianet
import re

class GNCharge():
    def __init__(self, order, **connection_params):
        self.order = order
        self.connection_params = connection_params

    @property
    def cleaned_billing_address(self):
        cep = re.sub("\D", "", self.order.billing_address.postal_code)

        if len(cep) != 8:
            raise InvalidZipcode
        return {
            'street': self.order.billing_address.street_address_1,
            'number': '123A',
            'neighborhood': 'Freguesia do O',
            'zipcode': cep,
            'city': self.order.billing_address.city,
            'state': self.order.billing_address.country_area
        }
    
    @property
    def cleaned_customer(self):
        # FIXME 
        # CPF HARDCODE???
        return {
            'name': self.order.billing_address.full_name,
            'cpf': '22790142890',
            'email': self.order.user_email,
            'phone_number': '11988044463',
            'birth': '2000-01-01'            
        }
    
    @property
    def cleaned_shippings(self):
        cleaned_shippings = []
        if self.order.shipping_method_name is not None:
            shipping_obj = {
                'name': self.order.shipping_method_name[:255],
                'value': int(self.order.shipping_price_gross.amount * 100)
            }
            cleaned_shippings.append(shipping_obj)
        return cleaned_shippings
        
    @property
    def cleaned_products(self):
        order_lines = self.order.lines.all()
        cleaned_products = []
        for product_line in order_lines:
            if product_line.product_name is None or len(product_line.product_name) < 1:
                continue
            if product_line.unit_price_gross.amount is None or product_line.unit_price_gross.amount < 0:
                continue
            product_obj = {
                'name': product_line.product_name[:255],
                'value': int(product_line.unit_price_gross.amount * 100)
            }
            if product_line.quantity is not None and product_line.quantity > 0:
                product_obj['amount'] = product_line.quantity
            cleaned_products.append(product_obj)
        return cleaned_products


    def pay_charge(self, **payment_data):
        params = {
            'id': payment_data['charge_id']
        }

        body = {
            'payment': {
                'credit_card': {
                    'installments': 1,
                    'payment_token': payment_data['card_token'],
                    'billing_address': self.cleaned_billing_address,
                    'customer': self.cleaned_customer
                }
            }
        }
        gn = Gerencianet(self.connection_params)

        returned_data = gn.pay_charge(params=params, body=body)

        return  returned_data

    def create_charge(self):
        if len(self.cleaned_products) == 0:
            raise EmptyProducts

        request_content = {'items': self.cleaned_products}

        if len(self.cleaned_shippings) != 0:
            request_content['shippings'] = self.cleaned_shippings

        gn = Gerencianet(self.connection_params)

        returned_data = gn.create_charge(body=request_content)

        return  returned_data