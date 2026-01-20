from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.http import JsonResponse
import pandas as pd
from .models import Recipe
from .forms import RecipesSearchForm, AddRecipeForm 
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

class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = AddRecipeForm
    template_name = 'recipes/add_recipe.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

@login_required
def profile(request):
    user = request.user
    authored_recipes = user.recipes.all()
    favorite_recipes = user.favorite_recipes.all()

    context = {
        'user': user,
        'authored_recipes': authored_recipes,
        'favorite_recipes': favorite_recipes
    }

    return render(request, 'recipes/profile.html', context)

class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    form_class = AddRecipeForm
    template_name = 'recipes/add_recipe.html'

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author

class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    template_name = 'recipes/confirm_delete.html'
    success_url = reverse_lazy('recipes:profile')

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author

@login_required
def toggle_favorite(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if request.user in recipe.favorited_by.all():
        recipe.favorited_by.remove(request.user)
        is_favorited = False
    else:
        recipe.favorited_by.add(request.user)
        is_favorited = True
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'is_favorited': is_favorited})
    
    return redirect('recipes:detail', pk=pk)