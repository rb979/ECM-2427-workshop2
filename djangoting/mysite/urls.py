"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/addItem', views.add_item, name='add_item'),
    path('api/v1/removeItem', views.remove_item, name='remove_item'),
    path('api/v1/removeItems', views.remove_items, name='remove_items'),
    path('api/v1/newType', views.new_type, name='new_type'),
    path('api/v1/removeType', views.remove_type, name='remove_type'),
    path('api/v1/addToShoppingList', views.add_to_shopping_list, name='add_to_shopping_list'),
    path('api/v1/removeFromShoppingList', views.remove_from_shopping_list, name='remove_from_shopping_list'),
    path('api/v1/purchaseItem', views.purchase_item, name='purchase_item'),
]

