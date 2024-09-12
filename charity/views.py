from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum
from django.shortcuts import render
from django.views import View
from .models import Donation, Institution


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


class AddDonationView(View):
    def get(self, request):
        return render(request, 'charity/form.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'charity/login.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'charity/register.html')