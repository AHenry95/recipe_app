from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import pandas as pd
from .models import Recipe
from .forms import RecipesSearchForm 
from .utils import get_chart

# Create your views here.
def home(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/home.html', {'recipes': recipes})

class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/list.html'
    context_object_name = 'recipes'

class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = 'recipes/detail.html'
    context_object_name = 'recipe'

@login_required
def search(request):
    form = RecipesSearchForm(request.POST or None)
    recipes_df = None
    chart = None

    if request.method == 'POST' and form.is_valid():
        recipe_name = form.cleaned_data['recipe_name']
        ingredient = form.cleaned_data['ingredient']
        difficulty = form.cleaned_data['difficulty']
        max_cooking_time = form.cleaned_data['max_cooking_time']
        chart_type = form.cleaned_data['chart_type']

        qs = Recipe.objects.all()

        if recipe_name:
            qs = qs.filter(name__icontains=recipe_name)
        
        if ingredient:
            qs = qs.filter(ingredients__icontains=ingredient)

        if difficulty:
            qs = qs.filter(difficulty=difficulty)

        if max_cooking_time:
            qs = qs.filter(cooking_time__lte=max_cooking_time)

        if qs.exists():
            data = []
            for recipe in qs:
                data.append({
                    'Name': f'<a href="{recipe.get_absolute_url()}">{recipe.name}</a>',
                    'Cooking Time': f'{recipe.cooking_time} min',
                    'Difficulty': recipe.difficulty
                })
            
            recipes_df = pd.DataFrame(data)
            recipes_df = recipes_df.to_html(escape=False, index=False, classes='results-table')

            chart_data = pd.DataFrame({
                'name': [recipe.name for recipe in qs],
                'cooking_time': [recipe.cooking_time for recipe in qs],
                'difficulty': [recipe.difficulty for recipe in qs],
                'ingredient_count': [len(recipe.get_ingredients_list()) for recipe in qs]
            })

            chart = get_chart(chart_type, chart_data)

    context={
        'form': form,
        'recipes_df': recipes_df,
        'chart': chart
    }

    return render(request, 'recipes/search.html', context)