from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone 
import datetime

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    month = models.IntegerField(default=datetime.datetime.now().month)
    year = models.IntegerField(default=datetime.datetime.now().year)
    amount = models.DecimalField(max_digits=50, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.category.name} - {self.month}/{self.year} - ${self.amount}"

class Category(models.Model):
    INCOME = 'Income'
    EXPENSE = 'Expense'

    CATEGORY_TYPES = [
        (INCOME, 'Income'),
        (EXPENSE, 'Expense'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # <-- Allow NULL for defaults
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=7, choices=CATEGORY_TYPES)
    is_default = models.BooleanField(default=False)  # <-- New field!

    def __str__(self):
        return f"{self.name} ({self.type})"

class Entry(models.Model):
    ENTRY_TYPES = (
        ('Income', 'Income'),
        ('Expense', 'Expense'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    entry_type = models.CharField(max_length=7, choices=ENTRY_TYPES)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.amount} ({self.entry_type})"
