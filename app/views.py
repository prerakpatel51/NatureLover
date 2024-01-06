from django.shortcuts import render,redirect
from django.views import View
import numpy as np
from .models import Customer,Product,Cart,OrderPlaced
from .forms import CustomerRegisterationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# def home(request):
#     return render(request, 'app/home.html')
class ProductView(View):
    def get(self,request):
        totalitem=0
        normal=Product.objects.filter(category='N')
        medicinals= Product.objects.filter(category='M')
        tools= Product.objects.filter(category='T')
        religious= Product.objects.filter(category='R')
        seeds= Product.objects.filter(category='S')
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
        return render(request,'app/home.html',
                      {'medicinals':medicinals,'tools':tools,'religious':religious,'seeds':seeds ,'normal':normal,'totalitem':totalitem})



# def product_detail(request):
#  return render(request, 'app/productdetail.html')

class ProductDetailView(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))

        item_already_in_cart=False
        if request.user.is_authenticated:
            item_already_in_cart=Cart.objects.filter(Q(product=product.id)& Q(user=request.user)).exists()

        return render(request,'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart,'totalitem':totalitem})
    
    
@login_required
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')


@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user =request.user
        cart=Cart.objects.filter(user=user)
        amount=0.0
        shipping_amount=40.0
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))

        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==user]
        if cart_product:
            for p in cart_product:
                tempamount=(p.quantity*p.product.discounted_price)
                amount+=tempamount
                totalamount=amount +shipping_amount
            return render(request, 'app/addtocart.html',{"carts":cart,'totalamount':totalamount,'amount':amount,'totalitem':totalitem})
          
        else:
            return render(request,'app/emptycart.html',{'totalitem':totalitem})  
        
        
        

def plus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
        c.quantity+=1
        c.save()
        amount=0.0
        
        shipping_amount=40.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
                tempamount=(p.quantity*p.product.discounted_price)
                amount+=tempamount
                # totalamount=amount 
        data={
                    'quantity':c.quantity,
                    'amount':amount,
                    'totalamount':amount+shipping_amount
                }
        return JsonResponse(data)


def minus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
        c.quantity-=1
        c.save()
        amount=0.0
        
        shipping_amount=40.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
                tempamount=(p.quantity*p.product.discounted_price)
                amount+=tempamount
                
        data={
                    'quantity':c.quantity,
                    'amount':amount ,
                    'totalamount':amount+shipping_amount
                }
        return JsonResponse(data)



def remove_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
        
        c.delete()
        amount=0.0
        
        shipping_amount=40.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
                tempamount=(p.quantity*p.product.discounted_price)
                amount+=tempamount
                
        data={
                    
                    'amount':amount,
                    'totalamount':amount+shipping_amount
                }
        return JsonResponse(data)






def about(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))

    return render(request,'app/about.html',{'totalitem':totalitem})










def buy_now(request):
 return render(request, 'app/buynow.html')

def profile(request):
    return render(request, 'app/profile.html')

def address(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))

    add=Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary','totalitem':totalitem})





@login_required
def orders(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))

    op=OrderPlaced.objects.filter(user=request.user)
    
    return render(request, 'app/orders.html',{'order_placed':op,'totalitem':totalitem})





def plants(request ,data=None):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))

    if data==None:
        plants=Product.objects.filter(category='N')    

    elif data=='Medicinals':
        plants=Product.objects.filter(category='M')
    elif data=='Tools':
        plants=Product.objects.filter(category='T')    
    elif data=='Seeds':
        plants=Product.objects.filter(category='S')    
    elif data=='Religious':
        plants=Product.objects.filter(category='R')    
    return render(request, 'app/plants.html' ,{'plants':plants,'totalitem':totalitem})

# def login(request):
#  return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')

class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegisterationForm()
        return render(request,'app/customerregistration.html',{'form':form})
    def post(self,request):
        form =CustomerRegisterationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations!! Registered Successfully')
            form.save()
        return render(request,'app/customerregistration.html',{'form':form})


@login_required
def checkout(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))

    user=request.user
    add =Customer.objects.filter(user=user)
    cart_items=Cart.objects.filter(user=user)
    amount=0.0
    shipping_amount=40.0
    totalamount=0.0
    cart_product=[p for p in Cart.objects.all() if p.user==request.user]
    if cart_product:
        for p in cart_product:
            tempamount=(p.quantity*p.product.discounted_price)
            amount+=tempamount
        totalamount=amount+shipping_amount
    return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items,'totalitem':totalitem})




@login_required
def payment_done(request):
    
    custid=request.GET.get('custid')
    user=request.user
    customer=Customer.objects.get(id=custid)
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect("orders")




# class based view hoi to ema avi rite lakhvanu  @method_decorator use kari ne  
@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        totalitem=0
        if request.user.is_authenticated:
          totalitem=len(Cart.objects.filter(user=request.user))

        form=CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary','totalitem':totalitem})
    def post(self,request):
        form =CustomerProfileForm(request.POST)
        if form.is_valid():
            usr=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            req=Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            req.save()
            messages.success(request,"congratulations Profile Updated Successfully")
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
    
    





# img khali jpg ma levi padse not working this way

# from keras.models import load_model
# from django.core.files.uploadedfile import InMemoryUploadedFile
# from io import BytesIO

# path='model/model.h5'
# cnn=load_model(path)
# def predict(request):
#     from keras.preprocessing import image
#     if request.method=='POST':
#         image=request.FILES.get('image1')
#         test_image = image.load_img(image,target_size=(64,64))
#         test_image = image.img_to_array(test_image)
#         test_image = np.expand_dims(test_image,axis=0)
#         result = cnn.predict(test_image)
        

#         if result[0][0]==1:
#             print('Daisy')
#             finalr='Daisy'
#         elif result[0][1]==1:
#             print('Dandelion')
#             finalr='Dandelion'

#         elif result[0][2]==1:
#             print('Rose')
#             finalr='Rose'
            
#         elif result[0][3]==1:
#             print('SunFlower')
#             finalr='SunFlower'
            
#         elif result[0][4]==1:
#             print("Tulip")
#             finalr='Tulip'
#         return render(request, 'app/prediction.html', {'prediction': finalr})

        
#     return render(request, 'app/predict.html')
    
    

import tensorflow as tf
import numpy as np
from keras.preprocessing.image import img_to_array
from keras.models import load_model





# -------- pellu model ----- #

pathh = 'model/model.h5'
cnn = load_model(pathh)
# pella model mate banayu

def predict(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))

    if request.method == 'POST':
        image_file = request.FILES.get('image1')
        # request ma thi image laisu pachi ene read karaisu ene tensorflow through decode karais and channels specify karis 3 red green ne black
        # agar file khali na hoi toj aa kaam karvanu 
        # tensorflow ne use kari ne resize karisu model na dimensions pramanay pelle ma 64x64 che bija ma 224x224 che ane tija ma 256x256 bani jai
        # pachi image ne array ma convert karisu 
        
        if image_file is not None:
            test_image = image_file.read()
            test_image = tf.image.decode_jpeg(test_image, channels=3)
            test_image = tf.image.resize(test_image, [64, 64])
            test_image = img_to_array(test_image)
            test_image = np.expand_dims(test_image, axis=0)
            result = cnn.predict(test_image)

            classes = ['Daisy', 'Dandelion', 'Rose', 'SunFlower', 'Tulip']
            finalr = classes[np.argmax(result)]
            # result 3 ayu hoi to aa eni array banave jema third element khali 1 hoi baki badha 0 emm ane ee je flower hase enu naam apse apda ne 
            
            print(finalr)
            
            return render(request, 'app/prediction.html', {'prediction': finalr,'totalitem':totalitem})
    #    tensorflow na tensor ma thi image_to_array use kari ne numpy array ma convert karis kemke keras khali numpy array j samje
    #    original image [64,64] mi hati ema hun add karis channels etle [64,64,3] have ek  batch size nu dimension add karis kemke model ma 4 dimensions che 
    return render(request, 'app/predict.html',{'totalitem':totalitem})

# -----------1 model no end---------------------




# bija model no code
path = 'model/model_inception.h5'
x = load_model(path)
def predict_cottondisease(request):
    totalitem=0
    if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))

    if request.method == 'POST':
        image_file = request.FILES.get('image1')
        if image_file is not None:
            test_image = image_file.read()
            test_image = tf.image.decode_jpeg(test_image, channels=3)
            
            # Resize the image while preserving aspect ratio
            test_image = tf.image.resize_with_pad(test_image, target_height=224, target_width=224)
            test_image = tf.cast(test_image, tf.float32) #integer ne float ma type cast 
            test_image = test_image / 255.0  # Normalize pixel values to [0, 1] stableize karva ma help karse aa vastu mane 
            
            test_image = np.expand_dims(test_image, axis=0)
            result = x.predict(test_image)

            classes = ['Diseased cotton leaf', 'Diseased cotton Plant', 'Fresh Cotton Plant', 'Fresh Cotton Leaf']
            finalr = classes[np.argmax(result)]
            print(finalr)

            # Optionally, you can return the result as a response or render it in a template
            # For example, using Django's JsonResponse to return the result as JSON
            return render(request, 'app/prediction_cottondisease.html', {'prediction': finalr})
    
    # Handle the case when the request method is not POST or image is not provided
    # You can return a default response or an error message here
    return render(request, 'app/predict_cottondisease.html',{'totalitem':totalitem})    
    

# ------------bija model no end-------------------






# -------------3 model ----------------


pat = 'model/all_disease_model.h5'
model = load_model(pat)

def predict_any_disease(request):
    totalitem=0
    if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))

    
    
    if request.method == 'POST':
        image_file = request.FILES.get('image1')
        if image_file is not None:
            test_image = image_file.read()
            test_image = tf.image.decode_jpeg(test_image, channels=3)
            
            # Resize the image while preserving aspect ratio
            test_image = tf.image.resize_with_pad(test_image, target_height=256, target_width=256)
            test_image = tf.cast(test_image, tf.float32)
            test_image = test_image / 255.0  # Normalize pixel values to [0, 1]
            
            test_image = np.expand_dims(test_image, axis=0)
            result = model.predict(test_image)

            classes = [
                'Apple leaf with scab disease',
                'Apple leaf with Blackrot disease',
                'Apple leaf with Cedar apple rust disease',
                'Healthy Apple leaf',
                'Healthy Blueberry leaf',
                'Healthy Cherry leaf',
                'Cherry leaf with Powdery mildew',
                'Corn leaf with Cercospora leaf spot contains gray spots on leaf ',
                'Corn leaf with common rust',
                'Healthy Corn leaf',
                'Corn leaf with Northern leaf blight',
                'Grape leaf with Black rot ',
                'Grape leaf with Esca Black measles',
                'Healthy Grape leaf ',
                'Grape leaf with Blight Isariopsis leaf spot',
                'Orange leaf with Haunglonbing also known as Citrus greening',
                'Peach leaf having Bacterial Spots',
                'Healthy Peach leaf',
                'Pepper leaf with Bacterial Spots',
                'Healthy Pepper leaf',
                'Potato leaf with Early Blight',
                'Healthy Potato leaf',
                'Potato leaf with Late Blight',
                'Healthy Raspberry leaf',
                'Healthy Soyabean leaf',
                'Squash leaf with Powdery mildew',
                'Healthy Strawberry leaf',
                'Strawberry leaf with Leaf Scroch',
                'Tomato leaf with Bacterial Spot',
                'Tomato leaf with Early Blight',
                'Healthy Tomato leaf ',
                'Tomato leaf with Late Blight ',
                'Tomato leaf with leaf Mold',
                'Tomato leaf with Septoria leaf Spot',
                'Tomato leaf with Spider Mites Two Spotted Spider Mite ',
                'Tomato leaf with Target Spot',
                'Tomato leaf with Mosaic Virus',
                 'Tomato leaf with Yellow Leaf Curl virus',
        ]
            finalr = classes[np.argmax(result)]
            print(finalr)

            # Optionally, you can return the result as a response or render it in a template
            # For example, using Django's JsonResponse to return the result as JSON
            return render(request, 'app/prediction_any_disease.html', {'prediction': finalr,'totalitem':totalitem})
    
    # Handle the case jyare image provide na karie tyare 
    
    return render(request, 'app/predict_any_disease.html',{'totalitem':totalitem})

# -----------3 model no end-------------------