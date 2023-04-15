from django.contrib import admin
from .models import (
    Customer,
    Product,
    
    OrderPlaced,
    Buy_single_product,
    payment_info,
    Transaction
)
# Register your models here.

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['id','user','name','locality','city','Zipcode','state']    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display =['id','title','discount_price','description_price','brand','category','product_image']

# @admin.register(Cart)
# class CartAdmin(admin.ModelAdmin):
#     list_display=['id','user','product','quantity']

@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display=['id','user','customer','product','quantity','order_date','status']    

@admin.register(Buy_single_product)
class Buy_single_productAdmin(admin.ModelAdmin):
    list_display=['id','user','product_id',]


@admin.register(payment_info)
class pay_infoAdmin(admin.ModelAdmin):
    list_display=['id']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display=['id']
