make migrations using python manage.py makemigrations Recipes
still need to set up superuser for the admin site, probably
uploaded the .csv file from WebAutomation
Recipe list can be seen at /recipes


IDEAS:
DONE Check ingredient stripping - make sure quantity and units are not being compared to
DONE look for NLP python libraries that identify food or numbers or units of measurement
add fuzzy matching to recipe_tree.py to see if that improves recommendations
DONE try kNN model to see if those recommendations are better
DONE if no NLP library, build something that gets rid of quantities and units

improve kNN matching to be less exact and provide a next best match
