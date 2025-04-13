from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Recipe

@admin.register(Recipe)
class RecipeAdmin(ImportExportModelAdmin):
    list_display = ('url_str', 'title', 'cook_time', 'description', 'directions', 'ingredients', 'prep_time',
                    'servings', 'total_time', 'date_added')