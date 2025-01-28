from django.db import models

class AmountType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=100)
    amount = models.PositiveIntegerField()
    amount_type = models.ForeignKey(AmountType, on_delete=models.CASCADE, related_name="items")

    def __str__(self):
        return f"{self.name} ({self.amount} {self.amount_type.name})"


class ShoppingList(models.Model):
    name = models.CharField(max_length=100)
    items = models.ManyToManyField(Item, related_name="shopping_lists")

    def __str__(self):
        return self.name
