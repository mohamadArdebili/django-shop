from apps.product.models import Product

CART_SESSION_ID = "cart"


class CartModule:
    """user's Cart using sessions """

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        cart = self.cart.copy()
        for item in cart.values():
            product = Product.objects.get(id=int(item["id"]))
            item["product"] = product
            item["total_price"] = int(item["quantity"]) * int(item["price"])
            item["unique_id"] = self.unique_id_generator(id=product.id, size=item["size"], color=item["color"])
            yield item

    def unique_id_generator(self, id, size, color):
        result = f"{id}-{size}-{color}"
        return result

    def add(self, product, quantity, size, color):
        unique_id = self.unique_id_generator(id=product.id, size=size, color=color)
        if unique_id not in self.cart:
            self.cart[unique_id] = {
                "quantity": 0,
                "price": str(product.price),
                "size": size,
                "color": color,
                "id": str(product.id)
            }
        self.cart[unique_id]["quantity"] += int(quantity)
        self.save()

    def delete(self, id):
        if id in self.cart:
            del self.cart[id]
            self.save()

    def remove_cart(self):
        del self.session[CART_SESSION_ID]

    def save(self):
        self.session.modified = True

    def total_price(self):
        cart = self.cart.values()
        total = sum(int(item["quantity"]) * int(item["price"]) for item in cart)
        return total
