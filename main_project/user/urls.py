from django.urls import path
from .views import *
urlpatterns = [
    path('userlogin/',Login.as_view(),name='userlogin'),
    path('signup/',Signup.as_view(),name='signup'),
    path('',Home.as_view(),name='userhome'),
    path('profile/',Profile.as_view(),name='userprofile'),
    path('editprofile/',EditProfile.as_view(),name='editprofile'),
    path('changepassword/',ChangePassword.as_view(),name='changepass'),
    path('edita ddress/<int:id1>/',EditAddress.as_view(),name='editaddress'),
    path('deladdress/<int:id>/',DeleteAddress.as_view(), name = 'deladdr'),
    path('orderstatchange/',OrderStatusChange.as_view(), name ='orderstatchange'),
    path('search/',Search.as_view(),name='usersearch'),
    path('addcart/<int:pk>/',AddCart.as_view(),name='addcart'),
    path('usercart/',UserCart.as_view(),name='usercart'),
    path('checkout/',Checkout.as_view(),name='checkout'),
    path('count/<int:id>/',Count.as_view(), name = 'count'),
    path('cartdelete/<int:id>/',CartDelete.as_view(), name = 'cartdelete'),
    path('chooseaddress/<int:id>',AddressChoose.as_view(),name='chooseaddress'),
    path('payment/',Payment.as_view(),name='payment'),
    path('stripepay/',Stripepay.as_view(),name='stripepay'),
    path('codpay/',Cod.as_view(),name='codpay'),
    path('successtr/',SuccessStripe.as_view(),name='successtr'),
    path('cancel/',CancelPayment.as_view(),name='cancel'),
    path('logout/',SignOut.as_view(),name='logout'),


]   