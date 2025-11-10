from django.urls import path
from . import views

app_name = "cart"
urlpatterns = [
    path("detail", views.CartDetailView.as_view(), name="cart_detail"),
    path("add/<int:pk>", views.CartAddView.as_view(), name="cart_add"),
    path("delete/<str:id>", views.CartDeleteView.as_view(), name="cart_delete"),
    path("order/<int:pk>", views.OrderDetailView.as_view(), name="order_detail"),
    path("order/add", views.OrderCreateView.as_view(), name="order_create"),
    path("apply-discount/<int:pk>", views.ApplyDiscountView.as_view(), name="apply_discount"),
    # Zarinpal payment gateway
    path("sendrequest/<int:pk>", views.SendRequestView.as_view(), name="send_request"),
    path("verify/", views.VerifyView.as_view(), name="verify_request"),
]
