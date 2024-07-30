# users/admin.py

from django.contrib import admin
from .models import User, Role, Category, SubCategory, Product

admin.site.register(User)
admin.site.register(Role)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
