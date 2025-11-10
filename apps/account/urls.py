from django.urls import path
from . import views

app_name = "account"
urlpatterns = [
    path("login", views.UserLoginView.as_view(), name="login"),
    path("register", views.OtpLoginView.as_view(), name="otp_login"),
    path("checkotp", views.CheckOtpView.as_view(), name="check_otp"),
    path("logout", views.logout_view, name="logout"),
    path("add/address", views.AddAddressView.as_view(), name="add_address"),
]
