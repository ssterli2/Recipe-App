from __future__ import unicode_literals
import requests
from django.db import models
from ..login_reg_app.models import User

class RecipeManage(models.Manager):
    def new_recipe(self, postData, user):
        if not Recipe.objects.filter(api_id=postData['id_input']).first():
            search = postData['id_input']
            params = {'key': '99573a05929673d2d785adb1d0a695c0', 'rId': search}
            r = requests.get('http://food2fork.com/api/get', params=params)
            rj = r.json()
            recipe = self.create(name=rj["recipe"]["title"], photo=rj["recipe"]["image_url"], publisher=rj["recipe"]["publisher"], api_id=rj["recipe"]["recipe_id"], recipe_link=rj["recipe"]["source_url"])
            userrecipe = UserRecipe.objects.create(recipe=recipe, user=user)
            for ingredient in rj["recipe"]["ingredients"]:
                response_from_ingred = Ingredient.objects.new_ingredient(ingredient)
                response_from_ingred["ingredient"].recipes.add(recipe)
        else:
            recipe = Recipe.objects.get(api_id=postData['id_input'])
            userrecipe = UserRecipe.objects.create(recipe=recipe, user=user)

    def unfavorite(self, postData, user):
        recipe = Recipe.objects.get(api_id=postData['id_input'])
        userrecipe = UserRecipe.objects.get(recipe=recipe, user=user)
        userrecipe.delete()

class IngredientManage(models.Manager):
    def new_ingredient(self, input_ingredient):
        ingredient = Ingredient.objects.filter(ingredient=input_ingredient).first()
        if not ingredient:
            ingredient = self.create(ingredient=input_ingredient)
        return {"ingredient" : ingredient}

class UserRecipeManage(models.Manager):
    def addcategory(self, postData, user):
        recipe = Recipe.objects.get(id=int(postData["recipeid"]))
        ur = UserRecipe.objects.filter(user=user, recipe=recipe).first()
        if postData["new_category"]:
            ur.category = postData["new_category"].lower()
            ur.save()
        elif postData["existing_category"]:
            ur.category = postData["existing_category"]
            ur.save()


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    photo = models.CharField(max_length=1000, default = '../static/images/default.jpg')
    publisher = models.CharField(max_length=100)
    api_id = models.CharField(max_length=100)
    recipe_link = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User, through="UserRecipe", related_name="recipes")
    objects = RecipeManage()

class UserRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, related_name="user_recipe")
    user = models.ForeignKey(User, related_name="user_recipe")
    category = models.CharField(max_length=100)
    objects = UserRecipeManage()

class Ingredient(models.Model):
    ingredient = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    recipes = models.ManyToManyField(Recipe, related_name="ingredients")
    objects = IngredientManage()
