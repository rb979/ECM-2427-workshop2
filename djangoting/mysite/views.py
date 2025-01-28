from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import AmountType, Item, ShoppingList


# View for creating a shopping list
def create_shopping_list(request):
    if request.method == "POST":
        list_name = request.POST.get("name")  # Get the shopping list name from POST data
        if not list_name:
            return JsonResponse({"error": "List name is required"}, status=400)

        shopping_list = ShoppingList.objects.create(name=list_name)
        return JsonResponse({"message": f"Shopping list '{shopping_list.name}' created", "id": shopping_list.id})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)


# Add item to list
def add_item_to_list(request, list_id):
    shopping_list = get_object_or_404(ShoppingList, id=list_id)
    if request.method == "POST":
        item_id = request.POST.get("item_id")
        item = get_object_or_404(Item, id=item_id)
        shopping_list.items.add(item)
        return JsonResponse({"message": f"Item '{item.name}' added to list '{shopping_list.name}'"})
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)


# Remove item from list
def remove_item_from_list(request, list_id, item_id):
    shopping_list = get_object_or_404(ShoppingList, id=list_id)
    item = get_object_or_404(Item, id=item_id)
    shopping_list.items.remove(item)
    return JsonResponse({"message": f"Item '{item.name}' removed from list '{shopping_list.name}'"})


# View to list all items in the shopping list
def list_items(request, list_id):
    shopping_list = get_object_or_404(ShoppingList, id=list_id)
    items = shopping_list.items.all()
    items_data = [{"id": item.id, "name": item.name, "amount": item.amount, "amount_type": item.amount_type.name} for item in items]
    return JsonResponse({"list_name": shopping_list.name, "items": items_data})
