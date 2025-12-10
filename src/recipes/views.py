from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Recipe

# Create your views here.
def home(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/home.html', {'recipes': recipes})

class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/list.html'
    context_object_name = 'recipes'

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/detail.html'
    context_object_name = 'recipe'