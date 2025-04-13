from django.db import models

class Recipe(models.Model):
    url_str = models.URLField()
    title = models.CharField(max_length=100)
    cook_time = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    directions = models.CharField(max_length=1000)
    # images = models.ImageField()
    ingredients = models.CharField(max_length=1000)
    prep_time = models.CharField(max_length=50)
    servings = models.CharField(max_length=5)
    total_time = models.CharField(max_length=50)
    date_added = models.DateTimeField()