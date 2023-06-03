from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
import datetime
import json
from .utils import cookieCart, cartData, guestOrder
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserProfileUpdateForm, UserRegistrationForm, UserLoginForm, ProductForm
from django.views import View
from .models import Product
from django.db.models import Count
from django.contrib.auth.decorators import login_required
import re
from .models import SubscribedUsers
from django.core.mail import send_mail
from django.conf import settings


 # Create your views here.


def landingPage(request):
    return render(request, 'store/landingPage.html')


@login_required(login_url='loginPage')
def homePage(request):
    q = request.GET.get('q', None)
    items = ''
    if q is None or q is "":
        products = Product.objects.all()
    elif q is not None:
        products = Product.objects.filter(title_contains=q)

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    products = Product.objects.all()
    context = {'products' : products, 'cartItems' : cartItems, 'order' : order, 'products' : products}
    return render(request, 'store/homePage.html', context)



class CategoryView(View):
    def get(self, request, val):
        product = Product.objects.filter(category=val)
        name = Product.objects.filter(category=val)
        data = cartData(request)
        cartItems = data['cartItems']
        order = data['order']
        products = Product.objects.all()
        return render(request, 'store/category.html', locals())
    


class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request, 'store/categoryPage.html', locals())



@login_required(login_url='loginPage')
class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'store/productDetailPage.html', locals())


def registerPage(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():  
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("homePage")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = UserRegistrationForm()

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    products = Product.objects.all()
    context = {'form' : form, 'products' : products, 'cartItems' : cartItems, 'order' : order}
    return render (request, "store/register.html", context)



def loginPage(request):
    if request.method == 'POST':
        form  = UserLoginForm(request, request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("homePage")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = UserLoginForm()

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    products = Product.objects.all()
    context = {'form' : form, 'products' : products, 'cartItems' : cartItems, 'order' : order}
    return render(request, 'store/login.html', context)


def logoutPage(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect("landing")

        
@login_required(login_url='loginPage')
def userAccountPage(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    products = Product.objects.all()
    context = {'products' : products, 'cartItems' : cartItems, 'order' : order}
    return render(request, 'store/userAccount.html', context)



@login_required(login_url='loginPage')
def checkoutPage(request):
    return render(request, 'store/checkoutPage.html')

@login_required(login_url='loginPage')
def productDeatilsPage(request):
    return render(request, 'store/productDetails.html')


def addProduct(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product Added successfully.")
            return redirect("homePage")
        else:
            messages.error(request,"Error Ocuured during Product Upload, Please try again later.......")
    else:
        form = ProductForm()

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    products = Product.objects.all()
    context = {'form' : form, 'products' : products, 'cartItems' : cartItems, 'order' : order, 'products' : products}
    return render(request, 'store/addProductPage.html', context)



@login_required(login_url='loginPage')
def contactPage(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    products = Product.objects.all()
    context = {'products' : products, 'cartItems' : cartItems, 'order' : order}
    return render(request, 'store/contactPage.html', context)


@login_required(login_url='loginPage')
def mainPage(request):
    return render(request, 'store/homePage.html')

@login_required(login_url='loginPage')
def store(request):

    data = cartData(request)
    cartItems = data['cartItems']
    
    products = Product.objects.all()

    context = {'products' : products, 'cartItems' : cartItems}
    return  render(request, 'store/categoryPage.html', context)


@login_required(login_url='loginPage')
def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
       
    context = {'items' : items, 'order' : order, 'cartItems' : cartItems}
    return  render(request, 'store/cartPage.html', context)


@login_required(login_url='loginPage')
def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    context = {'items' : items, 'order' : order, 'cartItems' : cartItems}
    return  render(request, 'store/checkout3.html', context)



@login_required(login_url='loginPage')
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    
    if action == 'add':
	    orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
	    orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was Added', safe=False)

@login_required(login_url='loginPage')
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:   
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
            ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
            )
    return JsonResponse('Payment submitted..', safe=False)



def paymentComplete(request):
    body = json.loads(request.body)
    print('BODY:',body)
    return JsonResponse('Payment Successfully Completed', safe=False)




def index(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        email = post_data.get("email", None)
        name = post_data.get("name", None)
        subscribedUsers = SubscribedUsers()
        subscribedUsers.email = email
        subscribedUsers.name = name
        subscribedUsers.save()
        # send a confirmation mail
        subject = 'NewsLetter Subscription'
        message = 'Hello ' + name + ', Thanks for subscribing us. You will get notification of latest articles posted on our website. Please do not reply on this email.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail(subject, message, email_from, recipient_list)
        res = JsonResponse({'msg': 'Thanks. Subscribed Successfully!'})
        return res
    return render(request, 'store/feedback.html')



def validate_email(request): 
    email = request.POST.get("email", None)   
    if email is None:
        res = JsonResponse({'msg': 'Email is required.'})
    elif SubscribedUsers.objects.get(email = email):
        res = JsonResponse({'msg': 'Email Address already exists'})
    elif not re.match(r"^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$", email):
        res = JsonResponse({'msg': 'Invalid Email Address'})
    else:
        res = JsonResponse({'msg': ''})
    return res


def sendEmailMessage(request):
    if request.method == 'POST':
        message = request.POST['message']

        send_mail(
            'Hello',
            message,
            settings.EMAIL_HOST_USER,
            ['engrahmadaya@gmail.com'],
            fail_silently=False
        )
    return render(request, 'store/contactPage.html')

 