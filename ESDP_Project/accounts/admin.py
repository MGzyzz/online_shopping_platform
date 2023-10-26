from django.contrib import admin
from accounts.models import User
from shop.models import Shop


# Register your models here.
class ShopInline(admin.StackedInline):
    model = Shop


class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', ]
    inlines = [ShopInline]


admin.site.register(User, UserAdmin)
