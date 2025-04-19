import re
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer

from .models import Recipe

recipes = Recipe.objects.all()


def clean_ingredients(ingredient_str):
    raw_ingredients = [i.strip().lower() for i in ingredient_str.split(',')]

    cleaned = []
    for ing in raw_ingredients:
        # Remove measurements ('1 tablespoon', '2 cups', etc.)
        ing = re.sub(r'^\d+[\d\s\/]*(?:[a-zA-Z]+\s)?', '', ing)
        cleaned.append(ing.strip())
    return cleaned

ingredient_lists = []
recipe_labels = []

for recipe in recipes:
    cleaned = clean_ingredients(recipe.ingredients)
    ingredient_lists.append(cleaned)
    recipe_labels.append(recipe.title)  # make a recipe id later and replace this

# convert ingredients to binary matrix using MultiLabelBinarizer
mlb = MultiLabelBinarizer()
x = mlb.fit_transform(ingredient_lists)
y = recipe_labels

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

clf = DecisionTreeClassifier()
clf.fit(x_train, y_train)

def match_recipe(user_ingredients):
    # Clean like we cleaned earlier
    cleaned_input = [i.lower().strip() for i in user_ingredients]
    vector = mlb.transform([cleaned_input])
    prediction = clf.predict(vector)
    return prediction[0]