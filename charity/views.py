from itertools import count

from django.db.models import Sum
from django.shortcuts import render
from django.views import View
from .models import Donation, Institution


class LandingPageView(View):
    def get(self, request):
        sum_of_donations = Donation.objects.aggregate(Sum('quantity'))
        count_of_donations = Donation.objects.distinct('institution').count
        foundations = Institution.objects.filter(type_of_institution='1')
        non_governmental = Institution.objects.filter(type_of_institution='2')
        locals_collections = Institution.objects.filter(type_of_institution='3')

        ctx = {
            'sum_of_donations': sum_of_donations['quantity__sum'],
            'count_of_donations': count_of_donations,
            'foundations': foundations,
            'non_governmental': non_governmental,
            'locals_collections': locals_collections,
        }
        return render(request, 'charity/index.html', ctx)


class AddDonationView(View):
    def get(self, request):
        return render(request, 'charity/form.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'charity/login.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'charity/register.html')