from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from tablib import Dataset
from django.http import HttpResponse
import csv, io
# from .recipe_tree import match_recipe
from .recipe_knn import match_recipe
from .resources import RecipeResource
from .forms import PantryForm, IngredientForm
from .models import PantryItem, Recipe
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
    if 'ingredients' not in request.session:
        request.session['ingredients'] = []

    ingredients = request.session['ingredients']
    form = IngredientForm(request.POST or None)
    recipe_title = None

    if request.method == 'POST':
        if 'add_item' in request.POST:
            if form.is_valid():
                new_ingredient = form.cleaned_data['ingredient'].strip().lower()
                if len(ingredients) <= 3:
                    ingredients.append(new_ingredient)
                    request.session.modified = True
                    print("Added:", new_ingredient) # save back to session
                    print('ingredients: ', ingredients)
                return redirect('recommend_recipe')

        elif 'delete_item' in request.POST:
            item_to_delete = request.POST.get('delete_item')
            if item_to_delete in ingredients:
                ingredients.remove(item_to_delete)
                request.session.modified = True
                print("Removed:", item_to_delete)
            return redirect('recommend_recipe')

        elif 'find_recipe' in request.POST:
            print("Find Recipe Clicked!")
            print("Current ingredients:", ingredients)
            if ingredients:
                best_match, next_best_match = match_recipe(ingredients)
                if best_match is not None:
                    best_ingredients = best_match.ingredients.split(',')
                    best_title = best_match.title
                    print('found best match')

                else:
                    best_ingredients = None
                    best_title = None
                    print('did not find best match')
                if next_best_match is not None:
                    next_best_ing = next_best_match.ingredients
                    next_best_title = next_best_match.title
                    print('found next best match')
                else:
                    next_best_ing = None
                    next_best_title = None
                    print('did not find next best match')

                context = {
                    'form': form,
                    'cooking_ingredients': ingredients,
                    'best_recipe_title': best_title,
                    'best_recipe_ingredients': best_ingredients,
                    'next_best_title': next_best_title,
                    'next_best_ingredients': next_best_ing
                }
                return render(request, 'recommend_recipe.html', context)

        elif 'clear_session' in request.POST:
            request.session['ingredients'] = []
            request.session.modified = True
            print("Session cleared!")
            return redirect('recommend_recipe')

    context = {
        'form': form,
        'cooking_ingredients': ingredients,
    }

    return render(request, 'recommend_recipe.html', context)

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