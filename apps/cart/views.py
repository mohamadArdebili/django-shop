from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.account.models import Address
from apps.cart.models import Order, OrderItem, Discount
from apps.product.models import Product
from apps.cart.cart_modules import CartModule
import requests
import json


class CartDetailView(LoginRequiredMixin, View):
    def get(self, request):
        cart = CartModule(request)
        return render(request, "cart/cart_detail.html", {"cart": cart})


class CartAddView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        print(product.id)
        size, color, quantity = request.POST.get("size", "-"), request.POST.get("color", "-"), request.POST.get(
            "quantity")
        cart = CartModule(request)
        cart.add(product=product, quantity=quantity, size=size, color=color)
        # print(size, color, quantity, product, product.id)
        return redirect("cart:cart_detail")


class CartDeleteView(View):
    def get(self, request, id):
        cart = CartModule(request)
        cart.delete(id=id)

        return redirect("cart:cart_detail")


class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = CartModule(request)
        order = Order.objects.create(user=request.user, total_price=cart.total_price())
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item["product"],
                color=item["color"],
                size=item["size"],
                quantity=item["quantity"],
                price=item["price"]
            )

        cart.remove_cart()
        return redirect("cart:order_detail", order.id)


class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        return render(request, "cart/order_detail.html", {"order": order})


class ApplyDiscountView(LoginRequiredMixin, View):
    def post(self, request, pk):
        """apply discount to order with given pk"""
        order = get_object_or_404(Order, id=pk)
        code = request.POST.get("discount")
        discount = get_object_or_404(Discount, name=code)
        if discount.quantity != 0:
            order.total_price -= order.total_price * (discount.discount / 100)
            order.save()
            discount.quantity -= 1
            discount.save()
            return redirect("cart:order_detail", order.id)
        else:
            return redirect("cart:order_detail", order.id)


# ZARINPAL
MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
amount = 11000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional
# Important: need to edit for real server.
CallbackURL = 'http://127.0.0.1:8080/cart/verify/'


class SendRequestView(View):
    def post(self, request, pk):
        order = get_object_or_404(Order, id=pk, user=request.user)
        address = get_object_or_404(Address, id=request.POST.get("address"))
        order.address = f"{address.address} - {address.zip_code} - {address.phone}"
        order.save()
        request.session["order_id"] = str(order.id)
        req_data = {
            "merchant_id": MERCHANT,
            "amount": order.total_price,
            "callback_url": CallbackURL,
            "description": description,
            "metadata": {"mobile": request.user.phone}
        }
        req_header = {"accept": "application/json",
                      "content-type": "application/json"}
        req = requests.post(
            url=ZP_API_REQUEST,
            data=json.dumps(req_data),
            headers=req_header
        )
        authority = req.json()['data']['authority']
        if len(req.json()['errors']) == 0:
            return redirect(ZP_API_STARTPAY.format(authority=authority))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


class VerifyView(View):
    def get(self, request):
        t_status = request.GET.get('Status')
        t_authority = request.GET['Authority']
        order_id = request.session["order_id"]
        order = Order.objects.get(id=int(order_id))
        if request.GET.get('Status') == 'OK':
            req_header = {"accept": "application/json",
                          "content-type": "application/json'"}
            req_data = {
                "merchant_id": MERCHANT,
                "amount": order.total_price,
                "authority": t_authority
            }
            req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
            if len(req.json()['errors']) == 0:
                t_status = req.json()['data']['code']
                if t_status == 100:
                    order.is_paid = True
                    order.save()
                    return HttpResponse('Transaction success.\nRefID: ' + str(
                        req.json()['data']['ref_id']
                    ))
                elif t_status == 101:
                    return HttpResponse('Transaction submitted : ' + str(
                        req.json()['data']['message']
                    ))
                else:
                    return HttpResponse('Transaction failed.\nStatus: ' + str(
                        req.json()['data']['message']
                    ))
            else:
                e_code = req.json()['errors']['code']
                e_message = req.json()['errors']['message']
                return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
        else:
            return HttpResponse('Transaction failed or canceled by user')
