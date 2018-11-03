from gerencianet import Gerencianet

class GNCharge():
    def __init__(self, order, **connection_params):
        self.order = order
        self.connection_params = connection_params

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


    def create_and_get_id(self):
        if len(self.cleaned_products) == 0:
            raise EmptyProducts

        request_content = {'items': self.cleaned_products}

        if len(self.cleaned_shippings) != 0:
            request_content['shippings'] = self.cleaned_shippings

        gn = Gerencianet(self.connection_params)

        returned_data = gn.create_charge(body=request_content)

        if returned_data['code'] != 200:
            raise GerencianetBadReturn
        return  returned_data['data']['charge_id']