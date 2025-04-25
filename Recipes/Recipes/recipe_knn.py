import re
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from rapidfuzz import process
from .models import Recipe

def clean_ingredients(ingredient_str):
    return [re.sub(r'^\d+[\d\s\/]*(?:[a-zA-Z]+\s)?', '', i.strip().lower()) for i in ingredient_str.split(',')]

def train_knn_model():
    recipes = list(Recipe.objects.all())

    ingredient_lists = []
    recipe_ids = []
    recipe_dict = {}

    for recipe in recipes:
        cleaned = clean_ingredients(recipe.ingredients)
        ingredient_lists.append(cleaned)
        recipe_ids.append(recipe.id)
        recipe_dict[recipe.id] = recipe

    mlb = MultiLabelBinarizer()
    x = mlb.fit_transform(ingredient_lists)
    y = recipe_ids

    model = KNeighborsClassifier(n_neighbors=1, metric='jaccard')  # Can adjust k if needed
    model.fit(x, y)

    return model, mlb, recipe_dict

def fuzzy_match(user_ingredients, known_ingredients):
    matched = []
    for ing in user_ingredients:
        match = process.extractOne(ing, known_ingredients, score_cutoff=80)
        if match:
            matched.append(match[0])
    return matched

def recommend_recipe(user_ingredients):
    model, mlb, recipe_dict = train_knn_model()
    known_ingredients = mlb.classes_

    cleaned_input = [i.lower().strip() for i in user_ingredients]
    fuzzy_matched_input = fuzzy_match(cleaned_input, known_ingredients)

    if not fuzzy_matched_input:
        return None, None, 0.0

    try:
        input_vector = mlb.transform([fuzzy_matched_input])
    except ValueError:
        return None, None, 0.0

    predicted_id = model.predict(input_vector)[0]
    matched_recipe = recipe_dict.get(predicted_id)

    # Compute match confidence: ratio of input ingredients matched
    if matched_recipe:
        recipe_ingredients = clean_ingredients(matched_recipe.ingredients)
        matched_count = sum(1 for ing in fuzzy_matched_input if ing in recipe_ingredients)
        confidence = matched_count / len(fuzzy_matched_input)
        print("Confidence", confidence)
        return matched_recipe, fuzzy_matched_input, confidence

    return None, None, 0.0