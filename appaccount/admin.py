from django.contrib import admin
from .models import Category, Product

from .models import Category, Product, SubCategory, Order


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
    )

    search_fields = (
        'name',
    )

    ordering = (
        'name',
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'category',
        'subcategory',
        'price',
        'old_price',
        'color',
        'size',
        'gender',
        'available',
        'created_at',
    )

    list_filter = (
        'category',
        'subcategory',
        'gender',
        'available',
        'created_at',
    )

    search_fields = (
        'name',
        'short_description',
        'description',
        'color',
        'subcategory__name',
    )

    list_editable = (
        'price',
        'available',
    )

    ordering = (
        '-created_at',
    )




from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'full_name',
        'phone',
        'product',
        'quantity',
        'total_amount',
        'payment_method',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'payment_method',
        'created_at',
    )

    search_fields = (
        'full_name',
        'phone',
        'email',
        'product__name',
        'pincode',
    )

    list_editable = (
        'status',
    )

    readonly_fields = (
        'created_at',
    )

    ordering = ('-created_at',)




@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'category',
    )

    list_filter = (
        'category',
    )

    search_fields = (
        'name',
    )

    ordering = (
        'name',
    )














from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'subject',
        'created_at',
        'is_read',
    )

    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_editable = ('is_read',)
    readonly_fields = ('created_at',)

    ordering = ('-created_at',)