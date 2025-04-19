import re

def clean_ingredient(ingredient):
    return re.sub(r'\d+[^a-zA-Z]+|[^a-zA-Z\s]', '', ingredient).strip().lower()