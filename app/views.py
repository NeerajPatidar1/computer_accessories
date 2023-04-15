from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product,  OrderPlaced , Buy_single_product ,Transaction  , payment_info
from .forms import CustomerRegistrationForm , CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required 
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.csrf import csrf_exempt  
from django.conf import settings
from .paytm import generate_checksum  , verify_checksum


class ProductView(View):
    def get(self,request):
        totalitem = 0
        topwears =Product.objects.filter(category='TW')
        bottomwears =Product.objects.filter(category='BW')
        mobiles =Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        return render(request, 'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles,'laptops':laptops,'totalitem':totalitem})


class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'app/productdetail.html',{'product':product})

@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order_placed':op})

class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request, 'app/Customerregistration.html',{'form':form})
    
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! Registered Successfully')
            form.save()
        return render(request, 'app/customerregistration.html',{'form':form})

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html',{'form':form,'active':'btn-primary'})
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            Zipcode=form.cleaned_data['Zipcode']
            reg = Customer(user=usr,name=name,locality=locality,city=city,state=state,Zipcode=Zipcode)
            reg.save()
            messages.success(request, 'Congratulation!! Profile Updated Successfully')
        return render(request, 'app/Profile.html',{'form':form,'active':'btn-primary'})

def buy_single_pro(request):
    user=request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Buy_single_product(user=user,product_id=product).save()
    print(product)
    return redirect('/single_pro_price')

def single_pro_price(request):
    user=request.user
    add= Customer.objects.filter(user=user)
    singal_pay = Buy_single_product.objects.filter(user=user)
    shipping_amount = 70.0
    single= [p for p in Buy_single_product.objects.all() if p.user == request.user]
    if single:
        for x in single:
            amount = x.product_id.selling_price
            tempamount = x.product_id.selling_price + shipping_amount
            prod = x.product_id.title
            break

        totalamount =tempamount
        title = prod
        price = amount
        print('totalamount',totalamount)
    return render(request, 'app/buy_single_product.html',{'add':add,'totalamount':totalamount,'price':price,'title':title,'single':single})

def payment_single_item(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    prod_buy = Buy_single_product.objects.filter(user=user)
    for prod_ in prod_buy:
        OrderPlaced(user=user, customer=customer,product=prod_.product_id,quantity=prod_.quantity).save()    
    return redirect("buy_single")

def callback1(request):
    return render(request, 'callback1.html')

@csrf_exempt
def initiate_payment_for_single(request):
    if request.method == "GET":
        return render(request, 'app/payments/pay.html')
    try:
        username = request.POST['username']
        password = request.POST['password']
        user=request.user
        add= Customer.objects.filter(user=user)
        singal_pay = Buy_single_product.objects.filter(user=user)
        shipping_amount = 70.0
        single= [p for p in Buy_single_product.objects.all() if p.user == request.user]
        if single:
            for x in single:
                amount = x.product_id.selling_price
                tempamount = x.product_id.selling_price + shipping_amount
                prod = x.product_id.title
                break
            totalamount =tempamount
            title = prod
            price = amount
        print('totalamount',totalamount)
        print(str(totalamount))
        user = authenticate(request, username=username, password=password)
        if user is None:
            raise ValueError
        auth_login(request=request, user=user)
    except:
        return render(request, 'app/payments/pay.html', context={'error': 'Wrong Accound Details or amount'})

    transaction = Transaction.objects.create(made_by=user, amount=totalamount)
    transaction.save()
    sinlge_product = Buy_single_product.objects.all()
    sinlge_product.delete()
    merchant_key = settings.PAYTM_SECRET_KEY
    print(totalamount)
    print(str(totalamount))

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.email)),
        ('TXN_AMOUNT', str(totalamount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, settings.PAYTM_SECRET_KEY)
    
    transaction.checksum = checksum
    transaction.save()
    
    paytm_params['CHECKSUMHASH'] = checksum
    # print('SENT: ', checksum)
    return render(request, 'app/payments/redirect.html', context=paytm_params)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        paytm_checksum = ''
        print(request.body)
        print(request.POST)
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':

                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            print("Checksum Matched")
            received_data['message'] = "Checksum Matched"
            all_data=payment_info(pay_data=paytm_params).save()  
             
        else:
            print("Checksum Mismatched")
            received_data['message'] = "Checksum Mismatched"

        return render(request, 'app/paymentdone.html', context=received_data)
    return render(request, 'app/payments/callback1.html')
