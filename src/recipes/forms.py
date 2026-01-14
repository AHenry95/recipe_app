from django import forms

CHART_CHOICES = (
    ('#1', 'None'),
    ('#2', 'Bar chart'),
    ('#3', 'Pie chart'),
    ('#4', 'Line chart')
)

DIFFICULTY_CHOICES = (
    ('', 'Any'),
    ('Easy', 'Easy'),
    ('Medium', 'Medium'),
    ('Intermediate', 'Intermediate'),
    ('Hard', 'Hard')
)

class RecipesSearchForm(forms.Form):
    recipe_name = forms.CharField(max_length=120, required=False, label='Recipe Name')
    ingredient = forms.CharField(max_length=120, required=False, label='Ingredient')
    difficulty= forms.ChoiceField(choices=DIFFICULTY_CHOICES, required=False)
    max_cooking_time = forms.IntegerField(required=False, min_value=1, label='Max Cooking Time (minutes)')
    chart_type = forms.ChoiceField(choices=CHART_CHOICES)