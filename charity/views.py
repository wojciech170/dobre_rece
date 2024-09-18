from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.views import View
from .models import Donation, Institution, Category
from django.contrib import messages

from django.contrib.auth import get_user_model, authenticate, login, logout

User = get_user_model()


class LandingPageView(View):
    def get(self, request):
        sum_of_donations = Donation.objects.aggregate(Sum('quantity'))
        count_of_donations = Donation.objects.distinct('institution').count()
        institutions = Institution.objects.all()

        foundations_list = institutions.filter(type_of_institution=1).order_by('name')
        foundation_paginator = Paginator(foundations_list, 5)
        foundation_page = request.GET.get('foundation_page')
        try:
            foundations = foundation_paginator.page(foundation_page)
        except PageNotAnInteger:
            foundations = foundation_paginator.page(1)
        except EmptyPage:
            foundations = foundation_paginator.page(foundation_paginator.num_pages)

        non_governmental_list = institutions.filter(type_of_institution='2').order_by('name')
        non_governmental_paginator = Paginator(non_governmental_list, 5)
        non_governmental_page = request.GET.get('non_governmental_page')
        try:
            non_governmental = non_governmental_paginator.page(non_governmental_page)
        except PageNotAnInteger:
            non_governmental = non_governmental_paginator.page(1)
        except EmptyPage:
            non_governmental = non_governmental_paginator.page(non_governmental_paginator.num_pages)

        locals_collections_list = institutions.filter(type_of_institution='3').order_by('name')
        locals_collections_paginator = Paginator(locals_collections_list, 5)
        locals_collections_page = request.GET.get('locals_collections_page')
        try:
            locals_collections = locals_collections_paginator.page(locals_collections_page)
        except PageNotAnInteger:
            locals_collections = locals_collections_paginator.page(1)
        except EmptyPage:
            locals_collections = locals_collections_paginator.page(locals_collections_paginator.num_pages)

        ctx = {
            'sum_of_donations': sum_of_donations['quantity__sum'],
            'count_of_donations': count_of_donations,
            'foundations': foundations,
            'non_governmental': non_governmental,
            'locals_collections': locals_collections,
            'foundation_paginator': foundation_paginator,
            'non_governmental_paginator': non_governmental_paginator,
            'locals_collections_paginator': locals_collections_paginator,
        }
        return render(request, 'charity/index.html', ctx)


class AddDonationView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        ctx = {
            'categories': categories,
            'institutions': institutions,
        }
        return render(request, 'charity/form.html', ctx)


class LoginView(View):
    def get(self, request):
        return render(request, 'charity/login.html')

    def post(self, request):
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('landing')
        else:
            messages.error(request, 'Wygląda że nie ma takiego użytkownika')
            return redirect('register')


class RegisterView(View):
    def get(self, request):
        return render(request, 'charity/register.html')

    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password == password2:
            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(
                    username=email,
                    first_name=name,
                    last_name=surname,
                    email=email,
                    password=password,
                )
                user.save()
                return redirect('login')
            else:
                return render(
                    request,
                    'charity/register.html',
                    {
                        'error': 'Użytkownik z takim email już istnieje'
                    }
                )
        else:
            return render(request, 'charity/register.html', {'error': 'Hasła nie są takie same'})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('landing')


class ConfirmView(View):
    def get(self, request):
        return render(request, 'charity/form-confirmation.html')

    def post(self, request):
        try:
            categories = Category.objects.filter(name=request.POST.get('categories'))
            institutions = Institution.objects.get(id=request.POST.get('organization'))

            if (
                    not request.POST.get('bags') or
                    not request.POST.get('address') or
                    not request.POST.get('city') or
                    not request.POST.get('phone') or
                    not request.POST.get('postcode') or
                    not request.POST.get('data') or
                    not request.POST.get('time') or
                    not request.POST.get('more_info')
            ):
                raise ValidationError("Wszystkie pola muszą być wypełnione.")

            donation = Donation.objects.create(
                quantity=request.POST.get('bags'),
                institution=institutions,
                address=request.POST.get('address'),
                phone_number=request.POST.get('phone'),
                city=request.POST.get('city'),
                zip_code=request.POST.get('postcode'),
                pick_up_date=request.POST.get('data'),
                pick_up_time=request.POST.get('time'),
                pick_up_comment=request.POST.get('more_info'),
                user=request.user
            )

            donation.category.set(categories)
            donation.save()

            return redirect('confirmation')
        except ValidationError as e:
            return render(request, 'charity/form.html', {'error': e.message})
