import re
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
from .models import Recipe
from .nlp_filter import parse_ingredients

# recipes = Recipe.objects.all()


# def clean_ingredients(ingredient_str):
#     raw_ingredients = [i.strip().lower() for i in ingredient_str.split(',')]
#     cleaned = []
#     for ing in raw_ingredients:
#         print('raw_ingredients: ', raw_ingredients)
#         ing = re.sub(r'^\d+[\d\s\/]*(?:[a-zA-Z]+\s)?', '', ing)
#         cleaned.append(ing.strip())
#         print('each ingredient: ', ing)
#     print('cleaned: ', cleaned)
#     return cleaned

def train_model():
    recipes = Recipe.objects.all()
    for recipe in recipes:
        print(recipe.id, recipe.title)
    ingredient_lists = []
    recipe_ids = []

    for recipe in recipes:
        cleaned = parse_ingredients(recipe.ingredients)
        print("NEW CLEANED: ", cleaned)
        ingredient_lists.append(cleaned)
        print("CHECK IF NEEDED: ", ingredient_lists)
        recipe_ids.append(recipe.id)

    # convert ingredients to binary matrix using MultiLabelBinarizer
    mlb = MultiLabelBinarizer()
    x = mlb.fit_transform(ingredient_lists)
    y = recipe_ids

    clf = DecisionTreeClassifier()
    clf.fit(x, y)
    return clf, mlb, {recipe.id: recipe for recipe in recipes}


def match_recipe(user_ingredients):
    clf, mlb, recipes = train_model()
    cleaned_input = [i.lower().strip() for i in user_ingredients]
    try:
        vector = mlb.transform([cleaned_input])
    except ValueError:
        return None, None   # no match found

    prediction = clf.predict(vector)
    recipe_id = prediction[0]
    matched_recipe = Recipe.objects.get(id=recipe_id)
    print(matched_recipe.ingredients)
    if matched_recipe:
        return matched_recipe.title, matched_recipe.ingredients
    return None, None