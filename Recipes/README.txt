make migrations using python manage.py makemigrations Recipes
still need to set up superuser for the admin site, probably
uploaded the .csv file from WebAutomation
Recipe list can be seen at /recipes
make sure template names are correct when adding in any other pages
decision tree will be made at recipe_tree.py
^ I have a tutorial for this somewhere

IDEAS:
Check ingredient stripping - make sure quantity and units are not being compared to
look for NLP python libraries that identify food or numbers or units of measurement
add fuzzy matching to recipe_tree.py to see if that improves recommendations
try kNN model to see if those recommendations are better
if no NLP library, build something that gets rid of quantities and units
