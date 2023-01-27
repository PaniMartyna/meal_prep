from crispy_forms.bootstrap import InlineCheckboxes
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms

from preferences.models import MealSetting, UserProfile


class MealSettingsForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('meals',)

    meals = forms.ModelMultipleChoiceField(queryset=MealSetting.objects.all(),
                                           label="",
                                           widget=forms.CheckboxSelectMultiple,
                                           required=True)



