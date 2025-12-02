from django.test import TestCase
from .models import Recipe

# Create your tests here.
class RecipeModelTest(TestCase):
    def setUpTestData():
        Recipe.objects.create(
            name = 'Scrambled Eggs',
            ingredients = 'eggs, butter, salt',
            cooking_time = 5,
            instructions = 'Beat eggs, cook in butter, season with salt'
        )

    def setUp(self):
        self.recipe = Recipe.objects.get(id=1)

    def test_name_max_length(self):
        max_length = self.recipe._meta.get_field('name').max_length
        self.assertEqual(max_length, 120)

    def test_difficulty_max_length(self):
        max_length = self.recipe._meta.get_field('difficulty').max_length
        self.assertEqual(max_length, 20)
    
    def test_ingredients_help_text(self):
        help_text = self.recipe._meta.get_field('ingredients').help_text
        self.assertEqual(help_text, 'Enter each ingredient, separated by a comma')

    def test_cooking_time_help_text(self):
        help_text = self.recipe._meta.get_field('cooking_time').help_text
        self.assertEqual(help_text, 'In minutes')
    
    def test_str_representation(self):
        self.assertEqual(str(self.recipe), 'Recipe: Scrambled Eggs')

    def test_difficulty_easy(self):
        self.assertEqual(self.recipe.difficulty, 'Easy')

    def test_difficulty_medium(self):
        recipe = Recipe.objects.create(
            name = 'Fruit Salad',
            ingredients = 'apple, banana, orange, grapes',
            cooking_time = 5,
            instructions = 'Chop fruit and mix'
        )
        self.assertEqual(recipe.difficulty, 'Medium')
    
    def test_difficulty_intermediate(self):
        recipe = Recipe.objects.create(
            name = 'Boiled Potatoes',
            ingredients = 'potatoes, salt, water',
            cooking_time = 20,
            instructions = 'Boil potatoes until soft'
        )
        self.assertEqual(recipe.difficulty, 'Intermediate')

    def test_difficulty_hard(self):
        recipe = Recipe.objects.create(
            name = 'Beef Stew',
            ingredients = 'beef, potatoes, carrots, onions, broth',
            cooking_time = 60,
            instructions = 'Brown beef, add vegetables and broth, simmer'
        )
        self.assertEqual(recipe.difficulty, 'Hard')

    def test_difficulty_updates_on_save(self):
        self.assertEqual(self.recipe.difficulty, 'Easy')

        self.recipe.ingredients = 'eggs, buuter, salt, pepper, cheese'
        self.recipe.cooking_time = 15
        self.recipe.save()

        self.assertEqual(self.recipe.difficulty, 'Hard')