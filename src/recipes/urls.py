from django.urls import path
from .views import home, RecipeListView, RecipeDetailView, RecipeCreateView, RecipeUpdateView, RecipeDeleteView, search, profile, toggle_favorite

app_name = 'recipes'

urlpatterns = [
    path('', home, name='home'),
    path('list/', RecipeListView.as_view(), name='list'),
    path('list/<pk>/', RecipeDetailView.as_view(), name='detail'),
    path('list/<pk>/edit/', RecipeUpdateView.as_view(), name='edit'),
    path('list/<pk>/delete/', RecipeDeleteView.as_view(), name='delete'),
    path('list/<pk>/favorite/', toggle_favorite, name='favorite'),
    path('search/', search, name='search'),
    path('add/', RecipeCreateView.as_view(), name='add'),
    path('profile/', profile, name='profile')
]