from django.contrib import admin
from .models import(Customer,Product,Cart,OrderPlaced)
from django.utils.html import format_html
from django.urls import reverse
# Register your models here.
# admin pane ma je kai be dekhadvu hoi e ahiya lakhvanu to mare char vastu batavi che to char
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=['id','user','name','locality','city','zipcode','state']
    # list displau ma je hoi e tya table na form a dekhai apda ne 
    
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=['id','title','selling_price','discounted_price','description'
                  ,'brand','category','product_image']
    
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product','quantity']
      
@admin.register(OrderPlaced)
class OrderedPlacedModelAdmin(admin.ModelAdmin):
    list_display=['id','user','customer','customer_info','product','product_info','quantity',
                  'ordered_date','status']
    def customer_info(self,obj):
        link=reverse("admin:app_customer_change",args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>',link,obj.customer.name)
        # aa apde link banai customer info ni etle admin ma orderplaced ma thi sidhu tya javai customer par click kariye etle
    
    def product_info(self,obj):
        link=reverse("admin:app_product_change",args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>',link,obj.product.title)
        # same product info ni link banai