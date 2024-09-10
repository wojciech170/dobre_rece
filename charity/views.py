from django.shortcuts import render
from django.views import View



class LandingPageView(View):
    def get(self, request):
        return render(request, 'charity/index.html')


class AddDonationView(View):
    def get(self, request):
        return render(request, 'charity/form.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'charity/login.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'charity/register.html')