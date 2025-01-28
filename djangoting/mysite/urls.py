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
    path('create_shopping_list/', views.create_shopping_list, name='create_shopping_list'),
    path('add_item_to_list/<int:list_id>/', views.add_item_to_list, name='add_item_to_list'),
    path('remove_item_from_list/<int:list_id>/<int:item_id>/', views.remove_item_from_list, name='remove_item_from_list'),
    path('list_items/<int:list_id>/', views.list_items, name='list_items'),
]

