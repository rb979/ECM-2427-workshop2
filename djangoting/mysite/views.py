from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date
from django.views.decorators.csrf import csrf_exempt
import json

from .models import AmountType, Item, ShoppingList


# API Endpoints

@csrf_exempt
def add_item(request):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            item_type = data.get("itemType")
            expiration_date = data.get("expirationDate")
            amount = data.get("amount")

            if not all([item_type, expiration_date, amount]):
                return JsonResponse({"error": "Missing parameters: 'itemType', 'expirationDate', and 'amount' are required."}, status=400)

            try:
                expiration_date = parse_date(expiration_date)
                if not expiration_date:
                    return JsonResponse({"error": "Invalid 'expirationDate' format."}, status=400)
            except ValueError:
                return JsonResponse({"error": "Invalid 'expirationDate' format."}, status=400)

            amount_type = AmountType.objects.filter(name=item_type).first()
            if not amount_type:
                return JsonResponse({"error": f"Amount type '{item_type}' not found in the database."}, status=404)

            Item.objects.create(
                name=item_type,
                amount=amount,
                amount_type=amount_type,
                expiration_date=expiration_date 
            )
            return JsonResponse({"message": "Item added successfully"}, status=200)

        except Exception as e:
            return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method. Only PUT is allowed."}, status=405)



@csrf_exempt
def remove_item(request):
    if request.method == "DELETE":
        try:
            data = json.loads(request.body)
            item_id = data.get("ID")

            if not item_id:
                return JsonResponse({"error": "Missing ID parameter"}, status=400)

            item = get_object_or_404(Item, id=item_id)
            item.delete()
            return JsonResponse({"message": "Item removed successfully"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def remove_items(request):
    if request.method == "DELETE":
        try:
            data = json.loads(request.body)
            ids = [item.get("ID") for item in data]

            if not ids:
                return JsonResponse({"error": "Missing IDs parameter"}, status=400)

            items = Item.objects.filter(id__in=ids)
            count = items.count()
            items.delete()
            return JsonResponse({"message": f"{count} items removed successfully"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def new_type(request):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            barcode = data.get("unique barcode")
            name = data.get("name")
            amount_type_name = data.get("amount type")

            if not all([barcode, name, amount_type_name]):
                return JsonResponse({"error": "Missing parameters"}, status=400)

            AmountType.objects.create(name=name)
            return JsonResponse({"message": "New type created successfully"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def remove_type(request):
    if request.method == "DELETE":
        try:
            data = json.loads(request.body)
            barcode = data.get("unique barcode")

            if not barcode:
                return JsonResponse({"error": "Missing unique barcode parameter"}, status=400)

            amount_type = get_object_or_404(AmountType, name=barcode)
            if Item.objects.filter(amount_type=amount_type).exists():
                return JsonResponse({"error": "Cannot delete type with existing items"}, status=400)

            amount_type.delete()
            return JsonResponse({"message": "Type removed successfully"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def add_to_shopping_list(request):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            item_type = data.get("item type")
            amount = data.get("amount")

            if not all([item_type, amount]):
                return JsonResponse({"error": "Missing parameters"}, status=400)

            shopping_list, _ = ShoppingList.objects.get_or_create(name="Default Shopping List")
            item, created = Item.objects.get_or_create(name=item_type, amount_type_id=1)
            item.amount += amount if not created else amount
            item.save()
            shopping_list.items.add(item)

            return JsonResponse({"message": f"Item '{item_type}' added to the shopping list successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def remove_from_shopping_list(request):
    if request.method == "DELETE":
        try:
            data = json.loads(request.body)
            item_type = data.get("itemType")
            amount = data.get("amount")

            if not all([item_type, amount]):
                return JsonResponse({"error": "Missing parameters"}, status=400)

            shopping_list = get_object_or_404(ShoppingList, name="Default Shopping List")
            item = get_object_or_404(Item, name=item_type)

            if item.amount > amount:
                item.amount -= amount
                item.save()
            else:
                shopping_list.items.remove(item)
                item.delete()

            return JsonResponse({"message": f"Item '{item_type}' updated or removed successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def purchase_item(request):
    if request.method == "PATCH":
        try:
            data = json.loads(request.body)
            item_type = data.get("item type")
            amount = data.get("amount")
            expiration_date = data.get("expiration date")

            if not item_type or not amount or not expiration_date:
                return JsonResponse({"error": "Missing parameters: 'item type', 'amount', and 'expiration date' are required."}, status=400)

            try:
                expiration_date = parse_date(expiration_date)
                if not expiration_date:
                    return JsonResponse({"error": "Invalid date format for 'expiration date'."}, status=400)
            except ValueError:
                return JsonResponse({"error": "Invalid date format for 'expiration date'."}, status=400)

            shopping_list = ShoppingList.objects.filter(name="Default Shopping List").first()
            if not shopping_list:
                return JsonResponse({"error": "Shopping list not found."}, status=404)

            item = shopping_list.items.filter(name=item_type).first()
            if not item:
                return JsonResponse({"error": f"Item '{item_type}' not found in the shopping list."}, status=404)

            if item.amount > amount:
                item.amount -= amount
                item.save()
            else:
                shopping_list.items.remove(item)
                item.delete()

            new_item = Item.objects.create(
                name=item_type,
                amount=amount,
                amount_type=item.amount_type,
                expiration_date=expiration_date  # Ensure expiration_date is handled correctly
            )
            return JsonResponse({"message": "Item purchased and added to the fridge."}, status=200)

        except Exception as e:
            # Return a detailed error message for debugging
            return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)

    # Handle invalid request methods
    return JsonResponse({"error": "Invalid request method. Only PATCH is allowed."}, status=405)
