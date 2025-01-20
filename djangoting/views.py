# views.py

from django.shortcuts import render
from .models import ShoppingList, Item, ShoppingListItem
from django.http import JsonResponse

def create_shopping_list(request):
    shopping_list = ShoppingList.objects.create(name="My First List")
    
    # Example of adding items
    item1 = Item.objects.create(name="Apples", price=2.5)
    item2 = Item.objects.create(name="Bananas", price=1.8)
    
    ShoppingListItem.objects.create(shopping_list=shopping_list, item=item1, quantity=3)
    ShoppingListItem.objects.create(shopping_list=shopping_list, item=item2, quantity=2)
    
    return JsonResponse({"message": "Shopping list created successfully."})

def view_shopping_list(request, list_id):
    shopping_list = ShoppingList.objects.get(id=list_id)
    items = shopping_list.items.all()
    
    response_data = {
        "shopping_list_name": shopping_list.name,
        "items": [{"name": item.name, "quantity": item.shoppinglistitem.quantity} for item in items]
    }
    
    return JsonResponse(response_data)
