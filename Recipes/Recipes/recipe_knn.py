from sklearn.neighbors import NearestNeighbors
import numpy as np
import pandas as pd
from .nlp_filter import parse_ingredients
from .models import Recipe


def match_recipe(user_ingredients):
    print('check3: ', user_ingredients)

    recipes = Recipe.objects.all()
    if not recipes.exists():
        return None, None

    data = []
    recipe_objs = []
    for recipe in recipes:
        raw_ingredients = recipe.ingredients.split(',')
        cleaned = parse_ingredients([i.strip() for i in raw_ingredients])
        data.append(cleaned)    # groups of ingredients per recipe
        recipe_objs.append(recipe)

    # Build vocab
    vocab = sorted(set(i for sublist in data for i in sublist))

    def vectorize(ingredients):
        return [1 if i in ingredients else 0 for i in vocab]

    recipe_vectors = [vectorize(ing) for ing in data]
    user_vector = [vectorize(user_ingredients)]

    if sum(user_vector[0]) == 0:
        return None, None

    # Fit k-NN
    # knn = NearestNeighbors(n_neighbors=min(5, len(recipe_vectors)), metric='cosine')
    knn = NearestNeighbors(n_neighbors=5, metric='cosine')
    knn.fit(recipe_vectors)

    distances, indices = knn.kneighbors(user_vector)

    # Best match
    best = None
    for idx in indices[0]:
        if len(set(data[idx]) & set(user_ingredients)) == len(user_ingredients):
            best = recipe_objs[idx]
            print('check type2: ', type(best))
            break

    # Next best: look for one that matches exactly 2 ingredients
    next_best = None
    for idx in indices[0]:  # skip best match
        overlap = len(set(data[idx]) & set(user_ingredients))
        if overlap == 2 and recipe_objs[idx] != best:
            next_best = recipe_objs[idx]
            break
    print('check below: ')
    print(best, next_best)
    print(type(best), type(next_best))
    return best, next_best