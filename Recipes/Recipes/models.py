from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    url_str = models.URLField()
    title = models.CharField(max_length=100)
    cook_time = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    directions = models.CharField(max_length=1000)
    ingredients = models.CharField(max_length=1000)
    prep_time = models.CharField(max_length=50)
    servings = models.CharField(max_length=5)
    total_time = models.CharField(max_length=50)
    date_added = models.DateTimeField()

class PantryItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pantry_items')
    ingredient = models.CharField(max_length=100)
    def __str__(self):
        return self.ingredient
