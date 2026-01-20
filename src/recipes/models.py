from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User

# Create your models here.
class Recipe(models.Model):
    name = models.CharField(max_length=120)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='recipes')
    ingredients = models.TextField(help_text='Enter each ingredient, separated by a comma')
    cooking_time = models.IntegerField(help_text='In minutes')
    difficulty = models.CharField(max_length=20, blank=True)
    instructions = models.TextField()
    pic = models.ImageField(upload_to='recipes', default='no_picture.jpg')
    favorited_by = models.ManyToManyField(User, related_name='favorite_recipes', blank=True)

    def set_difficulty(self):
        ingredient_count = len(self.ingredients.split(','))

        if self.cooking_time < 10 and ingredient_count < 4:
            return 'Easy'
        elif self.cooking_time < 10 and ingredient_count >= 4:
            return 'Medium'
        elif self.cooking_time >= 10 and ingredient_count < 4:
            return 'Intermediate'
        else:
            return 'Hard'
        
    def save(self, *args, **kwargs):
        if self.ingredients and self.cooking_time:
            self.difficulty = self.set_difficulty()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'Recipe: {self.name}'
    
    def get_absolute_url(self):
        return reverse('recipes:detail', kwargs={'pk': self.pk})
    
    def get_ingredients_list(self):
        return[ingredient.strip() for ingredient in self.ingredients.split(',')]