from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User
import pandas as pd
from .models import Recipe
from .views import home, RecipeListView, RecipeDetailView, search
from .forms import RecipesSearchForm, CHART_CHOICES, DIFFICULTY_CHOICES
from .utils import get_chart

# Create your tests here.
class RecipeModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.easy_recipe = Recipe.objects.create(
            name = 'Scrambled Eggs',
            ingredients = 'eggs, butter, salt',
            cooking_time = 5,
            instructions = 'Beat eggs, cook in butter, season with salt'
        )

        cls.medium_recipe = Recipe.objects.create(
            name = 'Fruit Salad',
            ingredients = 'apple, banana, orange, grapes',
            cooking_time = 5,
            instructions = 'Chop fruit and mix'
        )

        cls.intermediate_recipe = Recipe.objects.create(
            name = 'Boiled Potatoes',
            ingredients = 'potatoes, salt, water',
            cooking_time = 20,
            instructions = 'Boil potatoes until soft'
        )

        cls.hard_recipe = Recipe.objects.create(
            name = 'Beef Stew',
            ingredients = 'beef, potatoes, carrots, onions, broth',
            cooking_time = 60,
            instructions = 'Brown beef, add vegetables and broth, simmer'
        )

    # Field tests 
    def test_name_max_length(self):
        max_length = self.easy_recipe._meta.get_field('name').max_length
        self.assertEqual(max_length, 120)

    def test_difficulty_max_length(self):
        max_length = self.easy_recipe._meta.get_field('difficulty').max_length
        self.assertEqual(max_length, 20)
    
    def test_ingredients_help_text(self):
        help_text = self.easy_recipe._meta.get_field('ingredients').help_text
        self.assertEqual(help_text, 'Enter each ingredient, separated by a comma')

    def test_cooking_time_help_text(self):
        help_text = self.easy_recipe._meta.get_field('cooking_time').help_text
        self.assertEqual(help_text, 'In minutes')

    def test_pic_default_value(self):
        self.assertEqual(self.easy_recipe.pic.name, 'no_picture.jpg')
    
    # String representation tests
    def test_str_representation(self):
        self.assertEqual(str(self.easy_recipe), 'Recipe: Scrambled Eggs')

    # Difficulty representation tests
    def test_difficulty_easy(self):
        self.assertEqual(self.easy_recipe.difficulty, 'Easy')

    def test_difficulty_medium(self):
        self.assertEqual(self.medium_recipe.difficulty, 'Medium')
    
    def test_difficulty_intermediate(self):
        self.assertEqual(self.intermediate_recipe.difficulty, 'Intermediate')

    def test_difficulty_hard(self):
        self.assertEqual(self.hard_recipe.difficulty, 'Hard')

    def test_difficulty_updates_on_save(self):
        recipe = Recipe.objects.create(
            name = 'Test Recipe',
            ingredients = 'a, b, c',
            cooking_time = 5,
            instructions = 'Test'
        )
        self.assertEqual(recipe.difficulty, 'Easy')

        # Check if difficulty updates
        recipe.ingredients = 'a, b, c, d, e'
        recipe.cooking_time = 15
        recipe.save()
        self.assertEqual(recipe.difficulty, 'Hard')

    # Model method tests
    def test_get_absolute_url(self):
        url = self.easy_recipe.get_absolute_url()
        self.assertEqual(url, f'/list/{self.easy_recipe.pk}/')

    def test_get_ingredients_list(self):
        ingredients = self.easy_recipe.get_ingredients_list()
        self.assertEqual(ingredients, ['eggs', 'butter', 'salt'])
    
    def test_get_ingredients_list_strips_whitespace(self):
        recipe = Recipe.objects.create(
            name = 'Whitespace Test',
            ingredients = '  apple  , banana  , cherry  ',
            cooking_time = 5,
            instructions = 'Test'
        )
        ingredients = recipe.get_ingredients_list()
        self.assertEqual(ingredients, ['apple', 'banana', 'cherry'])

# Form Tests 
class RecipesSearchFormTest(TestCase):
    
    def test_form_valid_with_only_chart_type(self):
        form = RecipesSearchForm(data={'chart_type': '#1'})
        self.assertTrue(form.is_valid())
    
    def test_form_valid_with_all_fields(self):
        form_data = {
            'recipe_name': 'Pasta',
            'ingredient': 'tomato',
            'difficulty': 'Easy',
            'max_cooking_time': 30,
            'chart_type': '#2'
        }
        form = RecipesSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_recipe_name_max_length(self):
        form = RecipesSearchForm()
        self.assertEqual(form.fields['recipe_name'].max_length, 120)
    
    def test_ingredient_max_length(self):
        form = RecipesSearchForm()
        self.assertEqual(form.fields['ingredient'].max_length, 120)
    
    def test_max_cooking_time_min_value(self):
        # Tests that cooking time must be a positive number
        form = RecipesSearchForm(data={
            'max_cooking_time': 0,
            'chart_type': '#1'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('max_cooking_time', form.errors)

    def test_difficulty_choices(self):
        form = RecipesSearchForm()
        self.assertEqual(form.fields['difficulty'].choices, list(DIFFICULTY_CHOICES))
    
    def test_chart_type_choices(self):
        form = RecipesSearchForm()
        self.assertEqual(form.fields['chart_type'].choices, list(CHART_CHOICES))


# URL Tests
class RecipeURLTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.recipe = Recipe.objects.create(
            name = 'Test Recipe',
            ingredients = 'a, b, c',
            cooking_time = 5,
            instructions = 'Test instructions'
        )
    
    def test_home_url_name(self):
        self.assertEqual(reverse('recipes:home'), '/')
    
    def test_list_url_name(self):
        self.assertEqual(reverse('recipes:list'), '/list/')
    
    def test_detail_url_name(self):
        self.assertEqual(reverse('recipes:detail', kwargs={'pk': self.recipe.pk}), f'/list/{self.recipe.pk}/')

    def test_search_url_name(self):
        self.assertEqual(reverse('recipes:search'), '/search/')
    
    def test_login_url_name(self):
        self.assertEqual(reverse('login'), '/login/')
    
    def test_logout_url_name(self):
        self.assertEqual(reverse('logout'), '/logout/')

# Home View Tests
class HomeViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        cls.recipe1 = Recipe.objects.create(
            name = 'Recipe One',
            ingredients = 'a, b, c',
            cooking_time = 5,
            instructions = 'Instructions one'
        )
        cls.recipe2 = Recipe.objects.create(
            name = 'Recipe Two',
            ingredients = 'd, e, f, g',
            cooking_time = 15,
            instructions = 'Instructions two'
        )
    
    def setUp(self):
        self.client = Client()
        self.response = self.client.get('/')
    
    def test_home_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'recipes/home.html')
    
    def test_home_view_lists_all_recipes(self):
        recipes = self.response.context['recipes']
        self.assertEqual(len(recipes), 2)
    
    def test_home_view_contains_recipe_names(self):
        self.assertContains(self.response, 'Recipe One')
        self.assertContains(self.response, 'Recipe Two')

    def test_home_view_contains_welcome_section(self):
        self.assertContains(self.response, 'Welcome to the Kitchen!')
    
    def test_home_view_contains_browse_button(self):
        self.assertContains(self.response, 'Browse All Recipes')

    def test_home_view_shows_login_prompt_for_anonymous(self):
        self.assertContains(self.response, 'to view recipe details')

    def test_home_view_no_login_prompt_for_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/')
        self.assertNotContains(response, 'to view recipe details')
    
    def test_home_view_recipe_cards_locked_for_anonymous(self):
        self.assertContains(self.response, 'class="recipe-card locked"')
    
    def test_home_view_recipe_cards_clickable_for_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/')
        self.assertContains(response, f'href="/list/{self.recipe1.pk}"')


# Test home view if there are no recipes
class HomeViewEmptyTest(TestCase):

    def test_home_view_empty_state(self):
        response = self.client.get('/')
        self.assertContains(response, 'No recipes yet')

# List View Tests 
class RecipeListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        cls.recipe1 = Recipe.objects.create(
            name = 'List Recipe One',
            ingredients = 'a, b, c',
            cooking_time = 5,
            instructions = 'Instructions one'
        )
        cls.recipe2 = Recipe.objects.create(
            name = 'List Recipe Two',
            ingredients = 'd, e, f, g',
            cooking_time = 15,
            instructions = 'Instructions two'
        )

    def setUp(self):
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')
        self.response = self.client.get('/list/')

    def test_list_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'recipes/list.html')

    def test_list_view_lists_all_recipes(self):
        recipes = self.response.context['recipes']
        self.assertEqual(len(recipes), 2)
    
    def test_list_view_contains_recipe_names(self):
        self.assertContains(self.response, 'List Recipe One')
        self.assertContains(self.response, 'List Recipe Two')

    def test_list_view_contains_page_title(self):
        self.assertContains(self.response, 'All Recipes')

    def test_list_view_contains_cooking_times(self):
        self.assertContains(self.response, '5 min')
        self.assertContains(self.response, '15 min')
    
    def test_list_view_contains_difficulty_badges(self):
        self.assertContains(self.response, 'Easy')
        self.assertContains(self.response, 'Hard')

    def test_list_view_recipe_links_to_detail(self):
        self.assertContains(self.response, f'/list/{self.recipe1.pk}')
        self.assertContains(self.response, f'/list/{self.recipe2.pk}')

# Tests that list view requires authentication
class RecipeListViewAuthTest(TestCase):

    def test_list_view_redirects_anonymous_user(self):
        response = self.client.get('/list/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)

    def test_list_view_redirect_includes_next(self):
        response = self.client.get('/list/')
        self.assertIn('next=/list/', response.url)

# Test list view if there are no recipes
class RecipeListViewEmptyTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def setUp(self):
        self.client.login(username='testuser', password='testpass123')

    def test_list_view_empty_state(self):
        response = self.client.get('/list/')
        self.assertContains(response, 'No recipes added yet')

# Detail View Tests 
class RecipeDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        cls.recipe = Recipe.objects.create(
            name = 'Detail Test Recipe',
            ingredients = 'flour, sugar, eggs, butter',
            cooking_time = 30,
            instructions = 'Mix ingredients. Bake at 350F for 25 minutes.'
        )

    def setUp(self):
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')
        self.response = self.client.get(f'/list/{self.recipe.pk}/')

    def test_detail_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'recipes/detail.html')
    
    def test_detail_view_correct_recipe(self):
        recipe = self.response.context['recipe']
        self.assertEqual(recipe.name, 'Detail Test Recipe')
    
    def test_detail_view_contains_recipe_name(self):
        self.assertContains(self.response, 'Detail Test Recipe')
    
    def test_detail_view_contains_cooking_time(self):
        self.assertContains(self.response, '30 minutes')

    def test_detail_view_contains_difficulty(self):
        self.assertContains(self.response, 'Hard')
    
    def test_detail_view_contains_ingredients_section(self):
        self.assertContains(self.response, 'Ingredients')
        self.assertContains(self.response, 'flour')
        self.assertContains(self.response, 'sugar')
        self.assertContains(self.response, 'eggs')
        self.assertContains(self.response, 'butter')
    
    def test_detail_view_contains_instructions_section(self):
        self.assertContains(self.response, 'Instructions')
        self.assertContains(self.response, 'Mix ingredients')
    
    def test_detail_view_contains_back_link(self):
        self.assertContains(self.response, 'Back to Recipe List')
        self.assertContains(self.response, reverse('recipes:list'))

# Test that detail view requires authentication
class RecipeDetailViewAuthTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.recipe = Recipe.objects.create(
            name='Auth Test Recipe',
            ingredients='a, b, c',
            cooking_time=10,
            instructions='Test'
        )
    
    def test_detail_view_redirects_anonymous_user(self):
        response = self.client.get(f'/list/{self.recipe.pk}/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)

# Test detail view for non-existent recipe
class RecipeDetailView404Test(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def setUp(self):
        self.client.login(username='testuser', password='testpass123')

    def test_detail_view_404_for_invalid_pk(self):
        response = self.client.get('/list/9999/')
        self.assertEqual(response.status_code, 404)

# Search View Tests

# Test that search view requires authentication
class SearchViewAuthTest(TestCase):

    def test_search_view_redirects_anonymous_user(self):
        response = self.client.get('/search/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)

class SearchViewTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        cls.pasta = Recipe.objects.create(
            name='Spaghetti Carbonara',
            ingredients='pasta, eggs, bacon, parmesan, pepper',
            cooking_time=25,
            instructions='Cook pasta, mix with eggs and bacon'
        )
        cls.salad = Recipe.objects.create(
            name='Garden Salad',
            ingredients='lettuce, tomato, cucumber',
            cooking_time=5,
            instructions='Chop and mix vegetables'
        )
        cls.stew = Recipe.objects.create(
            name='Beef Stew',
            ingredients='beef, potatoes, carrots, onions, broth',
            cooking_time=40,
            instructions='Brown beef, add vegetables, simmer'
        )

    def setUp(self):
        self.client.login(username='testuser', password='testpass123')
    
    def test_search_view_get_request(self):
        response = self.client.get('/search/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/search.html')
        self.assertIn('form', response.context)
        self.assertIsNone(response.context['recipes_df'])
        self.assertIsNone(response.context['chart'])
    
    def test_search_view_contains_form_fields(self):
        response = self.client.get('/search/')
        self.assertContains(response, 'Recipe Name')
        self.assertContains(response, 'Ingredient')
        self.assertContains(response, 'Difficulty')
        self.assertContains(response, 'Max Cooking Time')
    
    def test_search_by_recipe_name(self):
        response = self.client.post('/search/', {
            'recipe_name': 'Spaghetti',
            'chart_type': '#1'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['recipes_df'])
        self.assertContains(response, 'Spaghetti Carbonara')
        self.assertNotContains(response, 'Garden Salad')
    
    def test_search_by_ingredient(self):
        response = self.client.post('/search/', {
            'ingredient': 'tomato',
            'chart_type': '#1'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Garden Salad')
        self.assertNotContains(response, 'Spaghetti Carbonara')
    
    def test_search_by_difficulty(self):
        response = self.client.post('/search/', {
            'difficulty': 'Easy',
            'chart_type': '#1'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Garden Salad')
    
    def test_search_by_max_cooking_time(self):
        response = self.client.post('/search/', {
            'max_cooking_time': 10,
            'chart_type': '#1'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Garden Salad')
        self.assertNotContains(response, 'Spaghetti Carbonara')
        self.assertNotContains(response, 'Beef Stew')
    
    def test_search_combined_filters(self):
        response = self.client.post('/search/', {
            'ingredient': 'beef',
            'max_cooking_time': 120,
            'chart_type': '#1'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Beef Stew')
    
    def test_search_no_results(self):
        response = self.client.post('/search/', {
            'recipe_name': 'Nonexistent Recipe',
            'chart_type': '#1'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context['recipes_df'])
        self.assertContains(response, 'No recipe found matching your search')
    
    def test_search_case_insensitive(self):
        response = self.client.post('/search/', {
            'recipe_name': 'spaghetti',
            'chart_type': '#1'
        })
        self.assertContains(response, 'Spaghetti Carbonara')
    
    def test_search_results_contain_links(self):
        response = self.client.post('/search/', {
            'recipe_name': 'Spaghetti',
            'chart_type': '#1'
        })
        self.assertContains(response, f'href="{self.pasta.get_absolute_url()}"')

    def test_search_with_bar_chart(self):
        response = self.client.post('/search/', {
            'chart_type': '#2'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['chart'])
    
    def test_search_with_pie_chart(self):
        response = self.client.post('/search/', {
            'chart_type': '#3'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['chart'])
    
    def test_search_with_line_chart(self):
        response = self.client.post('/search/', {
            'chart_type': '#4'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['chart'])
    
    def test_search_with_no_chart(self):
        response = self.client.post('/search/', {
            'chart_type': '#1'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context['chart'])

# Authentication View Tests
class LoginViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_login_view_get_request(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/login.html')
        self.assertContains(response, 'Welcome Back!')
        self.assertContains(response, 'Sign in')
    
    def test_login_view_successful_login(self):
        response = self.client.post('/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/list/')
    
    def test_login_view_invalid_credentials(self):
        response = self.client.post('/login/', {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('error_message', response.context)
    
    def test_login_view_nonexistent_user(self):
        response = self.client.post('/login/', {
            'username': 'nonexistent',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'error')
    
    def test_login_view_empty_form(self):
        response = self.client.post('/login/', {
            'username': '',
            'password': ''
        })
        self.assertEqual(response.status_code, 200)
    
    def test_login_view_contains_back_to_home_link(self):
        response = self.client.get('/login/')
        self.assertContains(response, 'Back to Home')
    
    def test_login_view_shows_redirect_message(self):
        response = self.client.get('/login/?next=/list/')
        self.assertContains(response, 'Please log in to access')
    
class LogoutViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def setUp(self):
        self.client.login(username='testuser', password='testpass123')
    
    def test_logout_view_renders_success_page(self):
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/success.html')
    
    def test_logout_view_success_message(self):
        response = self.client.get('/logout/')
        self.assertContains(response, 'successfully logged out')

    def test_logout_view_contains_login_link(self):
        response = self.client.get('/logout/')
        self.assertContains(response, 'Log Back In')
    
    def test_logout_view_contains_home_link(self):
        response = self.client.get('/logout/')
        self.assertContains(response, 'Back to Home')
    
    def test_logout_actually_logs_out(self):
        self.client.get('/logout/')
        response = self.client.get('/list/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)

# Navigation Tests
class NavigationTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_nav_shows_login_for_anonymous(self):
        response = self.client.get('/')
        self.assertContains(response, 'Login')
        self.assertNotContains(response, 'Logout')

    def test_nav_shows_logout_for_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/')
        self.assertContains(response, 'Logout')

    def test_nav_shows_username_for_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/')
        self.assertContains(response, 'Hello testuser!')
    
    def test_nav_contains_search_link(self):
        response = self.client.get('/')
        self.assertContains(response, 'Search')

#Utils Tests
class ChartUtilsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.recipe_data = pd.DataFrame({
            'name': ['Recipe 1', 'Recipe 2'],
            'cooking_time': [10, 20],
            'difficulty': ['Easy', 'Hard'],
            'ingredient_count': [3, 5]
        })

    def test_get_chart_returns_none_for_type_1(self):
        result = get_chart('#1', self.recipe_data)
        self.assertIsNone(result)
    
    def test_get_chart_returns_string_for_bar_chart(self):
        result = get_chart('#2', self.recipe_data)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
    
    def test_get_chart_returns_string_for_pie_chart(self):
        result = get_chart('#3', self.recipe_data)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
    
    def test_get_chart_returns_string_for_line_chart(self):
        result = get_chart('#4', self.recipe_data)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
    
    def test_get_chart_returns_none_for_invalid_type(self):
        result = get_chart('#7', self.recipe_data)
        self.assertIsNone(result)

# Integration Tests
class UserFlowIntegrationTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        cls.recipe = Recipe.objects.create(
            name='Test Recipe',
            ingredients='a, b, c',
            cooking_time=10,
            instructions='Test instructions'
        )
    
    def test_anonymous_user_flow(self):
        # Visit home page
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        # Try to access recipe list
        response = self.client.get('/list/')
        self.assertEqual(response.status_code, 302)

        # Go to login page
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
    
    def test_authenticated_user_flow(self):
        # Login
        response = self.client.post('/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)

        # Access recipe list
        response = self.client.get('/list/')
        self.assertEqual(response.status_code, 200)

        # View recipe detail
        response = self.client.get(f'/list/{self.recipe.pk}/')
        self.assertEqual(response.status_code, 200)

        # Search for recipes
        response = self.client.post('/search/', {
            'recipe_name': 'Test',
            'chart_type': '#1'
        })
        self.assertEqual(response.status_code, 200)

        # Logout
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 200)

        # Verify logout success
        response = self.client.get('/list/')
        self.assertEqual(response.status_code, 302)
