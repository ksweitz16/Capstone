from django import forms
from .models import PantryItem

class PantryForm(forms.ModelForm):
    class Meta:
        model = PantryItem
        fields = ['ingredient']
        widgets = { 'ingredient': forms.TextInput(attrs={'placeholder': 'e.g. olive oil, garlic'}), }

class IngredientForm(forms.Form):
    class Meta:
        ingredients = forms.CharField( widget=forms.Textarea(attrs={"placeholder": "e.g., onion, garlic, black beans"}), label="Enter ingredients (comma-separated)" )