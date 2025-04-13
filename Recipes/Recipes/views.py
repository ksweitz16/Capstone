from django.shortcuts import render
from .models import Recipe
from .resources import RecipeResource
from django.contrib import messages
from tablib import Dataset
from django.http import HttpResponse
import csv, io

def upload(request):
    if request.method == 'POST':
        recipe_resource = RecipeResource()
        dataset = Dataset()
        new_recipe = request.FILES['myfile']

        if not new_recipe.name.endswith('csv'):
            messages.info(request, 'CSV Files Only')
            return render(request, 'home.html')
        else:
            messages.info(request, 'File upload successful')

        data_set = new_recipe.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=','):
            created = Recipe.objects.update_or_create(
                url_str=column[0],
                title=column[1],
                cook_time=column[2],
                description=column[3],
                directions=column[4],
                ingredients=column[5],
                prep_time=column[6],
                servings=column[7],
                total_time=column[8],
                date_added=column[9]
            )
    return render(request, 'home.html')


def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipe_list.html', {'recipes': recipes})