from typing import Any
from django.shortcuts import render,redirect,reverse
from django.views.generic import View,TemplateView
from django.contrib.auth.models import User
from django.contrib import messages
from admin1.models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,JsonResponse 
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
import stripe
from django.conf import settings
from django.contrib.sessions.models import Session


stripe.api_key=settings.STRIPE_SECRET_KEY

# Create your views here.


class Login(View):
    def get(self,request):
        try:
            message = request.GET.get('message')
            print(message)
            return  render(request,'login.html',{'message':message})
        except:
            return render(request,'login.html')
    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user:
           login(request,user)
           print(user.username)
           message='You are logged in'
           url = reverse('userhome')  # Replace 'userhome' with your actual URL pattern name
           url_with_message = url + '?message=' + message
           return redirect(url_with_message)
       
        else:
           messages.error(request,'username and password is wrong')
           return redirect('userlogin')

class Signup(View):
    def get(self,request):
        return render(request,'signup.html')
    def post(self,request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        if password == password_confirm:
            if User.objects.filter(username=username).exists():
                return JsonResponse('false3', safe=False) 
            elif User.objects.filter(email=email).exists():
                return JsonResponse('false4', safe=False)
            # elif User.objects.filter(number=number).exists():
            #     return JsonResponse('false4', safe=False)
            else:
                User.objects.create_user(username=username,email=email,password=password)
                return JsonResponse('true', safe=False)
        else:
            return JsonResponse('false', safe=False)


# @login_required(redirect_field_name='login') 

class Home(LoginRequiredMixin,View):
    login_url = '/userlogin/'
    def get(self,request):
        try:
            message = request.GET.get('message')
            print(message)
        except:
            products=Products.objects.all() 
            cart_obj = Cart.objects.filter(user=request.user)
            context={'products':products,'cartcount':cart_obj}
            return render(request,'home.html',context)
        products=Products.objects.all() 
        cart_obj = Cart.objects.filter(user=request.user)
        context={'products':products,'cartcount':cart_obj,'message':message}
        return render(request,'home.html',context)
    

class Profile(LoginRequiredMixin,View):
    login_url = '/userlogin/'
    def get(self,request):
        address_details=Address.objects.filter(aduser=request.user)
        order_details=Order.objects.filter(user_order=request.user)
        cart_obj = Cart.objects.filter(user=request.user)
        context={'address':address_details,'orders':order_details,'cartcount':cart_obj}
        return render(request,'profile.html',context)
    def post(self,request):
         if request.method == 'POST':
            Fullname = request.POST['fullname']
            pincode = request.POST['pincode']
            city = request.POST['city']
            state = request.POST['state']
            housename = request.POST['housename']
            landmark = request.POST['landmark']
            address = Address.objects.create(Full_name=Fullname,pinCode=pincode,city=city,
            state=state,HouseName=housename,landMark=landmark,aduser=request.user)  
            address.save()
            address_user=Address.objects.filter(aduser=request.user).last()
            address_id=address_user.id
            request.session['addressid']=address_id
            return redirect('userprofile')
    
class ChangePassword(LoginRequiredMixin,View): 
    login_url = '/userlogin/'
  
    def post(self,request):
        oldpass = request.POST['oldpass']
        newpass1 = request.POST['newpass']
        conpass = request.POST['conpass']
        user=authenticate(request,username=request.user.username,password=oldpass)
        if user:
            if newpass1==conpass:
                user.set_password(conpass)
                user.save()
                messages.success(request,'password changed')
                return JsonResponse('true',safe=False)
            else:
                    return JsonResponse('false',safe=False)
        else:
            return JsonResponse('false1',safe=False)
        
class EditProfile(LoginRequiredMixin,View): 
    login_url = '/userlogin/'
  
    def post(self,request):
        username1 = request.POST['username1']
        email1= request .POST['email1']
        if User.objects.filter(username=username1).exclude(id=request.user.id).exists():
            return JsonResponse('false3', safe=False) 
        elif User.objects.filter(email=email1).exclude(id=request.user.id).exists():
            return JsonResponse('false4', safe=False)
        else:
            User.objects.filter(id=request.user.id).update(username=username1,email=email1)
            return JsonResponse('true',safe=False)

class EditAddress(LoginRequiredMixin,View): 
    login_url = '/userlogin/'
    def post(self,request,id1):
        print('///////////')
        fullname = request.POST['fullname']
        pincode = request.POST['pincode']
        city = request.POST['city']
        state = request.POST['state']
        housename = request.POST['housename']
        landmark = request.POST['landmark']
        Address.objects.filter(id=id1).update(Full_name=fullname,pinCode=pincode,city=city,state=state,HouseName=housename,landMark=landmark)
        return redirect('userprofile')

class DeleteAddress(LoginRequiredMixin,View):
    login_url = '/userlogin/'
    def get(self,request,id):
        addr = Address.objects.get(id=id)
        if 'addressid' in request.session:
            del request.session['addressid']
            addr.delete()
            return JsonResponse('true',safe=False)
        else:
            addr.delete()
            return JsonResponse('true',safe=False)


class OrderStatusChange(LoginRequiredMixin,View):
    login_url = '/userlogin/'
    def post(self,request):
        values =request.POST['Value']
        id1 = request.POST['id1']
        orders = Order.objects.get(id=id1)
        orders.Status = values
        orders.save()
        return JsonResponse('true',safe=False) 
        

class Search(LoginRequiredMixin,View):
    login_url = '/userlogin/'

    def get(self,request):
        productdetails=Products.objects.all()
        cart_obj = Cart.objects.filter(user=request.user)
        if Cart.objects.filter(user=request.user).exists():
            usercart=Cart.objects.get(user=request.user)
            search1=request.GET['search']
            products=Products.objects.filter(name__icontains=search1)
            context={'productdetails':productdetails,'usercart':usercart,'products':products}    
            return render(request,'search.html',context)   
        search1=request.GET['search']
        products=Products.objects.filter(name__icontains=search1)
        context={'productdetails':productdetails,'products':products,'cartcount':cart_obj}
        return render(request,'search.html',context)


class AddCart(LoginRequiredMixin,View):
    login_url = '/userlogin/'
    def get(self,request,pk):
        productdetails=Products.objects.get(id=pk)
        user=request.user
        Mycart,created=Cart.objects.get_or_create(user=user,products=productdetails)
        Mycart.count +=1
        Mycart.save()
        return JsonResponse('true',safe=False)

class UserCart(LoginRequiredMixin,View):
    login_url = '/userlogin/'
    def get(self,request):
        current_user  = User.objects.get(id=request.user.id)  
        current_usercart = Cart.objects.filter(user=current_user)
        grandtotal=0
        for j in current_usercart:
            total=0
            product2 = Products.objects.get(id=j.products.id)             
            total = float(product2.price)*j.count
            Cart.objects.filter(id=j.id).update(Total=total)
            grandtotal = grandtotal+float(product2.price)*j.count
            print(grandtotal)
        current_usercart.update(grand_total=grandtotal)
        context = {'current_usercart':current_usercart ,'grandtotal':grandtotal,'cartcount':current_usercart}
        return render (request, 'cart.html',context)

class Count(LoginRequiredMixin,View):
    login_url = '/userlogin/'
    def get(self,request,id):
        action = request.GET['action']
        cart_field = Cart.objects.get(id=id)
        if action == 'plus':
            cart_field.count += 1

        elif cart_field.count != 1:
                cart_field.count -= 1
        else:
            pass
        cart_field.save()
        return JsonResponse('true',safe=False)
    
class CartDelete(LoginRequiredMixin,View):
    login_url = '/userlogin/'
    def get(self,request,id):
        car = Cart.objects.get(id=id)
        car.delete()
        return JsonResponse('true',safe=False)
    
class Checkout(LoginRequiredMixin,View):
    login_url = '/userlogin/'
    def get(self,request):
        current_usercart = Cart.objects.filter(user=request.user).first()
        cart_obj = Cart.objects.filter(user=request.user)
        user_address=Address.objects.filter(aduser=request.user)
        if 'addressid' in request.session:
            address_code = request.session['addressid']
            context={'current_usercart':current_usercart,'address':user_address,'cartcount':cart_obj,'address_code':address_code}
            return render(request,'checkout.html',context)
        context={'current_usercart':current_usercart,'address':user_address,'cartcount':cart_obj}
        return render(request,'checkout.html',context)
    def post(self,request):
         if request.method == 'POST':
            Fullname = request.POST['fullname']
            pincode = request.POST['pincode']
            city = request.POST['city']
            state = request.POST['state']   
            housename = request.POST['housename']
            landmark = request.POST['landmark']
            address = Address.objects.create(Full_name=Fullname,pinCode=pincode,city=city,
            state=state,HouseName=housename,landMark=landmark,aduser=request.user)  
            address.save()
            address_user=Address.objects.filter(aduser=request.user).last()
            address_id=address_user.id
            request.session['addressid']=address_id
            return redirect('checkout')

class AddressChoose(LoginRequiredMixin,View):
    login_url = '/userlogin/'

    def get(self,request,*args,**kwargs):
        address_id=self.kwargs['id']
        print('///////////////')
        request.session['addressid']=address_id
        return JsonResponse('true',safe=False)

class Payment(LoginRequiredMixin,View):
    login_url = '/userlogin/'

    def post(self,request,*args,**kwargs):
        value = request.POST['value']
        try: 
            request.session['addressid']
        except:
            print('/////////')
            return JsonResponse('false',safe=False)
        if value == 'razarpay':
            return JsonResponse('true',safe=False)
        elif value == 'stripe':
            return JsonResponse('true1',safe=False)
        elif value == 'cod':
            print('/////')
            return JsonResponse('true2',safe=False)
        return redirect('checkout')
    

    
class Stripepay(LoginRequiredMixin,View):
    login_url = '/userlogin/'

    def get(self,request,*args,**kwargs): 
        current_usercart = Cart.objects.filter(user=request.user).first()
        cartTotalAmount = current_usercart.grand_total

        price_data  = {
     'currency': 'inr',
    'unit_amount': cartTotalAmount*int(100),
    'product_data': {
        'name': 'Cart Total',
    },
}


        
        line_item = {
      'price_data': price_data,
    'quantity': 1,
}
        checkout_session = stripe.checkout.Session.create(
            line_items=[line_item],
            mode='payment',
            success_url='http://127.0.0.1:8000/successtr/',
            cancel_url='http://127.0.0.1:8000/cancel/',
        )
    
        return redirect(checkout_session.url, code=303)
    


class SuccessStripe(LoginRequiredMixin,View):
    login_url = '/userlogin/' 
    def get(self,request,*args,**kwargs):
        user=User.objects.get(id=request.user.id)
        address = request.session['addressid']
        address1 = Address.objects.get(id=address)
        cart=Cart.objects.filter(user=user)
        for c in cart:
            Order.objects.create(user_order=user,Product=c.products,address=address1,Qty=c.count,Price=c.count*c.products.price,Status="ordered",PaymentMethod="STRIPE")
            c.delete()
        return render(request,'ordersuccess.html')

class Cod(LoginRequiredMixin,View):
    login_url = '/userlogin/'

    def get(self,request,*args,**kwargs):
        user=User.objects.get(id=request.user.id)
        address = request.session['addressid']
        address1 = Address.objects.get(id=address)
        cart=Cart.objects.filter(user=user)
        for c in cart:
            Order.objects.create(user_order=user,Product=c.products,address=address1,Qty=c.count,Price=c.count*c.products.price,Status="ordered",PaymentMethod="COD")
            c.delete()
        return render(request,'ordersuccess.html') 

       
class CancelPayment(LoginRequiredMixin,TemplateView):
    login_url = '/userlogin/'
    template_name='ordercancel.html'  


class SignOut(LoginRequiredMixin,View):
    login_url = '/userlogin/'

    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('userlogin')