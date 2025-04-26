import spacy
import re


UNITS = {
    'cup', 'cups', 'c',
    'teaspoon', 'teaspoons', 'tsp',
    'tablespoon', 'tablespoons', 'tbsp',
    'ounce', 'ounces', 'oz',
    'gram', 'grams', 'g',
    'liter', 'liters', 'ml',
    'pound', 'pounds', 'lb','kg',
    'pinch', 'pinches'
}

DESCRIPTORS = {
    'chopped', 'minced', 'uncooked', 'canned',
    'drained', 'ground', 'low', 'sodium', 'fat',
    'fresh', 'diced', 'peeled', 'sliced',
    'organic', 'boneless', 'skinless', 'shredded',
    'cooked', 'raw', 'reduced', 'large', 'small',
    'optional', 'garnish', 'package', 'medium'
}

nlp = spacy.load("en_core_web_sm")

def parse_ingredients(raw_ingredients):
    print('before stripping: ', raw_ingredients)
    ingredient_list = [i.strip() for i in raw_ingredients if i.strip()]
    print("Raw input now:", ingredient_list)
    """
    Takes a list of raw ingredient strings and returns just ingredients (no quantities or descriptors).
    """
    def clean_ingredient(ingredient):
        # Remove leading quantities like '1/2', '.5', '2'
        ingredient = re.sub(r'^[.\d/]+\s*', '', ingredient)
        doc = nlp(ingredient)
        tokens = []
        for token in doc:
            word = token.text.lower()
            if word in UNITS or word in DESCRIPTORS:
                continue
            if token.pos_ in {'NOUN', 'PROPN', 'ADJ'}:
                tokens.append(word)
        return ' '.join(tokens).strip()

    # Clean all ingredients and remove duplicates
    cleaned = [clean_ingredient(ing) for ing in ingredient_list]
    # print("nlp cleaned: ", cleaned)
    # print("returning: ", list(set(filter(None, cleaned))))
    return list(set(filter(None, cleaned)))