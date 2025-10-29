from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, reverse
from django.utils.crypto import get_random_string
from django.views import View
from uuid import uuid4
from random import randint
from .models import User, Otp
from .forms import LoginForm, OtpLoginForm, CheckOtpForm


# def user_login(request):
#     return render(request, "account/login.html", context={})
class UserLoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "account/templates/account/login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd["username"], password=cd["password"])
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                form.add_error("username", "Invalid username or password")
        else:
            form.add_error("username", "Invalid user data")
        return render(request, "account/templates/account/login.html", {"form": form})


class OtpLoginView(View):
    def get(self, request):
        form = OtpLoginForm()
        return render(request, "account/templates/account/otp_login.html", {"form": form})

    def post(self, request):
        form = OtpLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            random_code = randint(1000, 9999)
            print(f"OTP: {random_code}")
            token = str(uuid4())
            Otp.objects.create(phone=cd["phone"], code=random_code, token=token)
            return redirect(reverse("account:check_otp") + f'?token={token}')
        else:
            form.add_error("phone", "Invalid user data")
        return render(request, "account/templates/account/otp_login.html", {"form": form})


class CheckOtpView(View):
    def get(self, request):
        form = CheckOtpForm()
        return render(request, "account/templates/account/check_otp.html", {"form": form})

    def post(self, request):
        form = CheckOtpForm(request.POST)
        token = request.GET.get("token")
        if form.is_valid():
            cd = form.cleaned_data
            user_code = cd["code"]
            if Otp.objects.filter(token=token, code=user_code).exists():
                otp = Otp.objects.get(token=token)
                user, is_created = User.objects.get_or_create(phone=otp.phone)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                otp.delete()
                return redirect("/")
        else:
            form.add_error("code", "Invalid data")
        return render(request, "account/templates/account/check_otp.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("/")
