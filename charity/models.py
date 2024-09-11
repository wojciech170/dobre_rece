from email.policy import default

from django.contrib.auth.models import User
from django.db import models

INST_TYPES = [
    ('1', 'Fundacja'),
    ('2', 'Organizacja pozarządowa'),
    ('3', 'Zbiórka lokalna')
]

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Institution(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    type_of_institution = models.CharField(choices=INST_TYPES, default='1', max_length=1)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.IntegerField()
    category = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
