from django.db import models


# Create your models here.
class Recipe(models.Model):
    name = models.CharField(max_length=120)
    ingredients = models.TextField(help_text='Enter each ingredient, separated by a comma')
    cooking_time = models.IntegerField(help_text='In minutes')
    difficulty = models.CharField(max_length=20, blank=True)
    instructions = models.TextField()

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