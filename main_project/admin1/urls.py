from django.urls import path
from .views import *
urlpatterns = [
     path('',Dash.as_view(),name='dash'),
     path('signin/',SignIn.as_view(),name='adminsignin'),
     path('addproduct/',AddProduct.as_view(),name='addprod'),
     path('viewcust/',ViewCustomer.as_view(),name='viewcus'),
     path('viewprod/',ViewProduct.as_view(),name='viewprod'),
     path('blockuser/<int:pk>/',BlockUser.as_view(),name='blockuser'),
     path('editprod/<int:id>',EditProd.as_view(),name='editprod'),
     path('delprod/<int:id>/',DelProd.as_view(),name='delprod'),
     path('vieworder/',ViewOrders.as_view(),name='vieworder'),
     path('orderchange/',OrderChange.as_view(),name='orderchange'),
     path('reports/',Reports.as_view(),name='reports'),
     path('signout/',SignOut.as_view(),name='signout'),

]