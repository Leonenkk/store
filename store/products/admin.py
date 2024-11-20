from django.contrib import admin

from products.models import ProductCategory, Product, Basket

admin.site.register(ProductCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    fields = ('name', ('price', 'quantity'), 'category', 'description', 'image')
    search_fields = ('name',)
    ordering = ('name',)


class BasketAdmin(admin.TabularInline):
    model = Basket
    extra = 1
    fields = ('product', 'quantity','created_timestamp')
    readonly_fields = ('created_timestamp',)



