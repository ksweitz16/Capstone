from django import forms
from .models import PantryItem

class PantryForm(forms.ModelForm):
    class Meta:
        model = PantryItem
        fields = ['ingredient']
        widgets = { 'ingredient': forms.TextInput(attrs={'placeholder': 'e.g. olive oil, garlic'}), }

class IngredientForm(forms.Form):
    ingredient = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. garlic'})
    )