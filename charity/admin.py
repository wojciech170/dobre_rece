from django.contrib import admin
from charity.models import Institution, Donation, Category

admin.site.register(Institution)
admin.site.register(Donation)
admin.site.register(Category)