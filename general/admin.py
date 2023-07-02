from django.contrib import admin
from .models import Vendor, Tool, Category, Tool_Category

# Register your models here.
admin.site.register(Vendor)
admin.site.register(Tool)
admin.site.register(Category)
admin.site.register(Tool_Category)