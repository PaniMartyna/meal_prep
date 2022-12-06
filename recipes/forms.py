from django import forms

from recipes.models import Recipe


class RecipeAddForm(forms.ModelForm):
    name = forms.CharField(label="", widget=forms.TextInput(attrs={
        'placeholder': 'nazwa dania',
        'autofocus': 'autofocus'
    }))
    portions = forms.IntegerField(label="", widget=forms.NumberInput(attrs={
        'placeholder': 'liczba porcji',
        'min': 1,
        'step': 0.5,
    }))
    ingredients = forms.CharField(label="", widget=forms.Textarea(attrs={
        'placeholder': 'składniki'
    }))
    method = forms.CharField(label="", widget=forms.Textarea(attrs={
        'placeholder': 'opis przygotowania'
    }))

    class Meta:
        model = Recipe
        fields = ['name', 'portions', 'ingredients', 'method']
