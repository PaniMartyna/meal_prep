from crispy_forms.bootstrap import InlineCheckboxes
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms

from preferences.models import MealSetting


class MealSettingsForm(forms.ModelForm):
    meals_list = MealSetting.objects.all()
    MEALS = [(str(meal.id), meal.meal_name) for meal in meals_list]

    class Meta:
        model = MealSetting
        fields = ['meal_name']

    meal_name = forms.MultipleChoiceField(choices=MEALS,
                                          label="",
                                          widget=forms.CheckboxSelectMultiple(),
                                          required=True,
                                          error_messages={
                                              'required': 'wybierz przynajmniej jeden posiłek, '
                                                          'żeby zacząć korzystać z funkcji planowania'
                                          })

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.layout = Layout(
    #         InlineCheckboxes('meals', css_class="btn btn-aubergine"),
    #         Submit('submit', 'zapisz', css_class='btn btn-aubergine')
    #         )
