from django.shortcuts import render,redirect
from user.models import *
from django.views.generic import View,CreateView,UpdateView,TemplateView
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse,JsonResponse 
from django.utils.decorators import method_decorator
from datetime import date

# Create your views here.

def SignInRequired(func):
    def wrapper(request,*args,**kwargs):
        if request.session.has_key('key'):
            return func(request,*args,**kwargs)
        else:
            return redirect('adminsignin')
    return wrapper


@method_decorator(SignInRequired,name='dispatch')
class Dash(View):
    def get(self,request):
        try:
            order = Order.objects.all()
            qty = order.count()
        except:
            qty=0
            #order count

        try:
            orderdelivered = Order.objects.filter(Status='delivered')
            qtydelivered = orderdelivered.count()
        except:
            qtydelivered=0    
           #order delivered count

        try:
            currentDate = date.today()
            orderstoday = Order.objects.filter(Date__day=currentDate.day)
            orderstoday=orderstoday.count()
        except:
            orderstoday=0
            #orders today
        
        try:
            currentDate = date.today()
            ordersdeltoday = Order.objects.filter(Date__day=currentDate.day,Status='delivered')
            ordersdeltoday=ordersdeltoday.count()
        except:
            ordersdeltoday=0
            #orders delivered today



        
        try:
            totalcustomers = User.objects.all()
            qtycustomers = totalcustomers.count()
        except:
            qtycustomers=0
            #total customers
        
        try:
            fullrevenue=0
            for i in orderdelivered:
                fullrevenue += i.Price
            netrevenue=fullrevenue
        except:
            netrevenue=0
            #net revenue

        try:
            currentDate = date.today()
            ordertoday = Order.objects.filter(Date__day=currentDate.day,Status='delivered')
            today=0
            for i in ordertoday:
                today = today + i.Price
            revenuetoday = today
        except:
            revenuetoday = 0
            #today's revenue
        
        try:
            currentmonth = currentDate.month
            currentmonthtext= date.today().strftime('%B')
            orderdate = Order.objects.filter(Date__month=currentmonth,Status='delivered')
            month=0
            for i in orderdate:
                month = month + i.Price
            revenuemonth = month
        except:
            revenuemonth=0
            #month revenue
        
        try:
            currentyear = currentDate.year
            orderyear = Order.objects.filter(Date__year=currentyear,Status='delivered')
            year=0
            for i in orderyear:
                year = year + i.Price
            revenueyear = year
        except:
            revenueyear=0
            #year revenue



        context={'qty':qty,'qtydelivered':qtydelivered,'netrevenue':netrevenue,'revenuetoday':revenuetoday,'revenuemonth':revenuemonth,
                'revenueyear':revenueyear,'qtycustomers':qtycustomers,'currentyear':currentyear,'currentmonthtext':currentmonthtext,'orderstoday':orderstoday,
                'ordersdeltoday':ordersdeltoday  }
        return render(request,'dashboard.html',context)
    
# @method_decorator(SignInRequired,name='dispatch')
class SignIn(View):
    def get(self,request):
        return render(request,'adlogin.html')
    def post(self,request):
            username = request.POST.get('username')
            password = request.POST.get('password')
            if (username =="finasvm" and password =="1234"):
                request.session['key'] = 'user'
                return redirect('dash')
            messages.success(request,'username and password is wrong')
            return redirect('adminsignin')
    
@method_decorator(SignInRequired,name='dispatch')
class ViewCustomer(View):
    def get(self,request):
        customers=User.objects.all()
        return render(request,'viewcustomers.html',{'customers':customers})

@method_decorator(SignInRequired,name='dispatch') 
class BlockUser(View):
    def get(self,request,pk):
        user_det=User.objects.get(id=pk)
        if user_det.is_active == True:
            user_det.is_active=False
            user_det.save()
            return redirect('viewcus')
        user_det.is_active=True
        user_det.save()
        return redirect('viewcus')
    

@method_decorator(SignInRequired,name='dispatch')
class ViewProduct(View):
    def get(rself,request):
        products=Products.objects.all()
        return render(request,'products.html',{'products':products})
        
         
@method_decorator(SignInRequired,name='dispatch')
class AddProduct(CreateView):
    model=Products
    form_class=ProductForm
    template_name='addproduct.html'
    success_url=reverse_lazy('dash')

    def form_valid(self, form):
            form.instance.user=self.request.user
            self.object = form.save()
            print(self.object)    
            return super().form_valid(form)

@method_decorator(SignInRequired,name='dispatch')
class EditProd(UpdateView):
    template_name='editproduct.html'
    form_class=ProductForm
    model=Products
    success_url=reverse_lazy('dash')
    pk_url_kwarg='id'

    def form_valid(self, form):
            """If the form is valid, save the associated model."""
            self.object = form.save()
            return super().form_valid(form)
    
class DelProd(View):
    def get(self,request,id):
        prod = Products.objects.get(id=id)
        prod.delete()
        return JsonResponse('true',safe=False)

@method_decorator(SignInRequired,name='dispatch')
class ViewOrders(View):   
    def get(self,request):
        order = Order.objects.all()
        return render(request,'vieworders.html',{'order':order})
    
class OrderChange(View):
    def post(self,request):
        print('/////////////')
        values =request.POST['Value']
        id1 = request.POST['id1']
        orders = Order.objects.get(id=id1)
        if values=='ship':
            orders.Status = 'shipped'
        elif values == 'deliver':
            orders.Status = 'delivered'
        orders.save()
        return JsonResponse('true',safe=False)
    
class Reports(View):
    def get(self,request):
        ordertable = Order.objects.all()
        return render(request,'report.html',{'orders':ordertable})
        
    def post(self,request):
        date1=request.POST['date1']
        date2=request.POST['date2'] 
        print(date1)
        ordertable = Order.objects.filter(Date__range=[date1,date2]) 
        return render(request,'report.html',{'orders':ordertable})  

class SignOut(View):
     def get(self,request,*args,**kwargs):
        del request.session['key']
        return redirect('adminsignin')