from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from tablib import Dataset
from django.http import HttpResponse
import csv, io
from .models import Recipe
from .recipe_tree import match_recipe
from .resources import RecipeResource
from .forms import PantryForm, IngredientForm
from.models import PantryItem
from .utils import clean_ingredient

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

def recommend_recipe_view(request):
    recipe_title = None
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            raw_ingredients = form.cleaned_data['ingredients']
            ingredient_list = [i.strip() for i in raw_ingredients.split(',')]
            recipe_title = match_recipe(ingredient_list)
    else:
        form = IngredientForm()
    return render(request, 'recommend_recipe.html', { 'form': form, 'recipe_title': recipe_title })

def pantry_view(request):
    pantry_items = PantryItem.objects.filter(user=request.user).order_by('ingredient')
    if request.method == 'POST':
        if 'add_item' in request.POST:
            form = PantryForm(request.POST)
            if form.is_valid():
                new_item = form.save(commit=False)
                new_item.user = request.user
                new_item.ingredient = clean_ingredient(new_item.ingredient)
                if not PantryItem.objects.filter(user=request.user, ingredient=new_item.ingredient).exists():
                    new_item.save()
                return redirect('pantry')

        elif 'delete_item' in request.POST:
            item_id = request.POST.get('item_id')
            PantryItem.objects.filter(id=item_id, user=request.user).delete()
            return redirect('pantry')

    else:
        form = PantryForm()

    return render(request, 'pantry.html', {
        'form': form,
        'pantry_items': pantry_items,
    })

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('pantry')  # or any other page
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})