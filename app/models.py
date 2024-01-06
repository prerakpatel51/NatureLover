from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator

# Create your models here.
# total char table banaya che apde ek default user model use karyu che

STATE_CHOICES=(
     ("Andhra Pradesh","Andhra Pradesh"),
     ("Arunachal Pradesh","Arunachal Pradesh"),
     ("Assam","Assam"),
     ("Bihar","Bihar"),
     ("Chhattisgarh","Chhattisgarh"),
     ("Goa","Goa"),
     ("Gujarat","Gujarat"),
     ("Haryana","Haryana"),
     ("Himachal Pradesh","Himachal Pradesh"),
     ("Jammu and Kashmir","Jammu and Kashmir"),
     ("Jharkhand","Jharkhand"),
     ("Karnataka","Karnataka"),
     ("Kerala","Kerala"),
     ("Madhya Pradesh","Madhya Pradesh"),
     ("Maharashtra","Maharashtra"),
     ("Manipur","Manipur"),
     ("Meghalaya","Meghalaya"),
     ("Mizoram","Mizoram"),
     ("Nagaland","Nagaland"),
     ("Odisha","Odisha",),
     ("Punjab","Punjab"),
     ("Rajasthan","Rajasthan"),
     ("Sikkim","Sikkim"),
     ("Tamil Nadu","Tamil Nadu"),
     ("Telangana","Telangana"),
     ("Tripura","Tripura"),
     ("Uttar Pradesh","Uttar Pradesh"),
     ("Uttarakhand","Uttarakhand"),
     ("West Bengal","West Bengal"),)

class Customer(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    # agar user ek jagya e delete karye to a badhe thi delete thai jai on_delete  thi 
    # built in User model use kariyu che apde 
    name =models.CharField(max_length=200)
    locality=models.CharField(max_length=200)
    city=models.CharField(max_length=50)
    zipcode =models.IntegerField()
    state=models.CharField(choices=STATE_CHOICES,max_length=50)
    # apde a method etle lakhie ke jena thi apdane khabar pade ke 
    # je customer nu instance print karaiye to human readable form ma print thai  
    def __str__(self):
        return str(self.id)
    
# By default, the User model includes karte che fields like username, email, password, first_name, ane last_name,and others. agar joitu hoi to customize karai you can extend it by creating a custom user model. Creating a custom user model is usually recommended when you have specific requirements beyond the built-in User model.








CATEGORY_CHOICES=(
    ('N','Normal'),
    ('M','Medicinal'),
    ("R",'Religious'),
    ("S",'Seeds'),
    ("T",'Tools'),
)    
class Product(models.Model):
    title=models.CharField(max_length=100)
    selling_price=models.FloatField()
    discounted_price=models.FloatField()
    description=models.TextField()
    brand=models.CharField(max_length=100)
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    product_image = models.ImageField(upload_to='productimg')
    # apde images ne statically j store karis ane productimg ma store karais khali e img ni url apde db ma store karaisu 
    
    def __str__(self):
        return str(self.id)
# ana thi alag alag product ne apde db ma store karisu 









class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE) 
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return str(self.id)
    
    @property
    def total_cost(self):
        return self.quantity*self.product.discounted_price
    # cart naam nu object hoi to agar ema vagar parenthissis apde totalcost no attribute  use kari sakie 
    # dynamically calculate kari sakie apde anathi totalcost
    
     






STATUS_CHOICES=(
    ('Accepted','Accepted'),('Packed','Packed'),('On The Way','On The Way'),('Delivered','Delivered'),('Cancel','Cancel')
    )    
class OrderPlaced(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    ordered_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')
    
    @property
    def total_cost(self):
        return self.quantity*self.product.discounted_price
    
# je je order karya hase ene apde db ma store karisu  
# apde ekaj user che ena alag alag address ane customer name hoi etle ene apde foreign key banai 