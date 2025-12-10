from django.test import TestCase, Client
from django.urls import reverse, resolve
from .models import Recipe
from .views import home, RecipeListView, RecipeDetailView

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

class RecipeURLTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.recipe = Recipe.objects.create(
            name = 'Test Recipe',
            ingredients = 'a, b, c',
            cooking_time = 5,
            instructions = 'Test instructions'
        )
    
    def test_home_url(self):
        url = resolve('/')
        self.assertEqual(url.func, home)

    def test_list_url(self):
        url = resolve('/list/')
        self.assertEqual(url.func.view_class, RecipeListView)
    
    def test_detail_url(self):
        url = resolve(f'/list/{self.recipe.pk}/')
        self.assertEqual(url.func.view_class, RecipeDetailView)
    
    def test_list_url_name(self):
        url = reverse('recipes:list')
        self.assertEqual(url, '/list/')
    
    def test_detail_url_name(self):
        url = reverse('recipes:detail', kwargs={'pk': self.recipe.pk})
        self.assertEqual(url, f'/list/{self.recipe.pk}/')

class HomeViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
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
    
    def test_home_view_contains_recipes_in_context(self):
        self.assertIn('recipes', self.response.context)
    
    def test_home_view_lists_all_recipes(self):
        recipes = self.response.context['recipes']
        self.assertEqual(len(recipes), 2)
    
    def test_home_view_contains_recipe_name(self):
        self.assertContains(self.response, 'Recipe One')
        self.assertContains(self.response, 'Recipe Two')

    def test_home_view_contains_welcome_section(self):
        self.assertContains(self.response, 'Welcome to the Kitchen!')
    
    def test_home_view_contains_navigation(self):
        self.assertContains(self.response, 'Home')
        self.assertContains(self.response, 'All Recipes')
    
    def test_home_view_contains_browse_button(self):
        self.assertContains(self.response, 'Browse All Recipes')

# Test home view if there are no recipes
class HomeViewEmptyTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.response = self.client.get('/')

    def test_home_view_empty_state(self):
        self.assertContains(self.response, 'No recipes yet')

class RecipeListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
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
        self.response = self.client.get('/list/')

    def test_list_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'recipes/list.html')
    
    def test_list_view_contains_recipes_in_context(self):
        self.assertIn('recipes', self.response.context)

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

# Test list view if there are no recipes
class RecipeListViewEmptyTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.response = self.client.get('/list/')

    def test_list_view_empty_state(self):
        self.assertContains(self.response, 'No recipes added yet')

class RecipeDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.recipe = Recipe.objects.create(
            name = 'Detail Test Recipe',
            ingredients = 'flour, sugar, eggs, butter',
            cooking_time = 30,
            instructions = 'Mix ingredients. Bake at 350F for 25 minutes.'
        )

    def setUp(self):
        self.client = Client()
        self.response = self.client.get(f'/list/{self.recipe.pk}/')

    def test_detail_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'recipes/detail.html')
    
    def test_detail_view_contains_recipe_in_context(self):
        self.assertIn('recipe', self.response.context)
    
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
    
    def test_detail_view_contains_navigation(self):
        self.assertContains(self.response, 'Home')
        self.assertContains(self.response, 'All Recipes')

# Test detail view for non-existent recipe
class RecipeDetailView404Test(TestCase):

    def setUp(self):
        self.client = Client()

    def test_detail_view_404_for_invalid_pk(self):
        response = self.client.get('/list/9999/')
        self.assertEqual(response.status_code, 404)