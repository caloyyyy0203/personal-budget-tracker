from django.contrib import admin
from .models import Entry, Category, Budget
# Register your models here.
admin.site.register(Entry)
admin.site.register(Category)
admin.site.register(Budget)