from crispy_forms.helper import FormHelper
from django import forms

from crispy_forms.layout import Layout, Row, Column, Submit
from crispy_forms.bootstrap import InlineCheckboxes
from django.core.exceptions import ValidationError

from recipes.models import Recipe, MealTag


def validate_recipe_exists(value):
    """checks if recipe under given name already exists"""
    recipe = Recipe.objects.filter(name=value)
    if recipe:  # check if any object exists
        raise ValidationError('taki przepis już istnieje w Twojej książce kucharskiej. Podaj inna nazwę')


class RecipeAddForm(forms.ModelForm):

    MEAL_TAG_CHOICES = [
        (1, 'śniadanie'),
        (2, 'przekąska'),
        (3, 'obiad'),
        (4, 'kolacja'),
        (5, 'zupa'),
        (6, 'deser'),
        (7, 'na drogę'),
    ]

    name = forms.CharField(label="",
                           widget=forms.TextInput(attrs={
                                'placeholder': 'nazwa dania',
                                'autofocus': 'autofocus'
                                }),
                           validators=[validate_recipe_exists])

    portions = forms.IntegerField(label="",
                                  widget=forms.NumberInput(attrs={
                                    'placeholder': 'liczba porcji',
                                    'min': 1,
                                    'step': 0.5,
                                     }))

    ingredients = forms.CharField(label="",
                                  widget=forms.Textarea(attrs={
                                    'placeholder': 'składniki'
                                    }))

    method = forms.CharField(label="",
                             required=False,
                             widget=forms.Textarea(attrs={
                                'placeholder': 'opis przygotowania',
                                }))

    meal_tags = forms.MultipleChoiceField(choices=MEAL_TAG_CHOICES,
                                          label="",
                                          widget=forms.CheckboxSelectMultiple(),
                                          required=True,
                                          error_messages={
                                              'required': 'wybierz przynajmniej jedną kategorię dla tego przepisu'
                                          })

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('portions', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            InlineCheckboxes('meal_tags'),
            'ingredients',
            'method',
            Submit('submit', 'zapisz', css_class='button is-warning')
            )

    class Meta:
        model = Recipe
        fields = ['name', 'portions', 'meal_tags', 'ingredients', 'method']


class RecipeEditForm(RecipeAddForm):

    name = forms.CharField(label="",
                           widget=forms.TextInput(attrs={
                                'placeholder': 'nazwa dania',
                                'autofocus': 'autofocus'
                                }),
                            )

