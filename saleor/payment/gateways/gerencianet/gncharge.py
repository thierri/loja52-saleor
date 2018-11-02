from gerencianet import Gerencianet

class GNCharge():
    def __init__(self, order, **connection_params):
        self.order = order

    def get_cleaned_products(self):
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