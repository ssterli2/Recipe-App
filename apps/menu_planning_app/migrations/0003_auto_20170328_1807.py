# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-28 18:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu_planning_app', '0002_recipe_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipeingredient',
            name='ingredient',
        ),
        migrations.RemoveField(
            model_name='recipeingredient',
            name='recipe',
        ),
        migrations.RenameField(
            model_name='recipe',
            old_name='api_link',
            new_name='api_id',
        ),
        migrations.AddField(
            model_name='ingredient',
            name='recipes',
            field=models.ManyToManyField(related_name='ingredients', to='menu_planning_app.Recipe'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='recipe_link',
            field=models.CharField(default=' ', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='ingredient',
            field=models.CharField(max_length=1000),
        ),
        migrations.DeleteModel(
            name='RecipeIngredient',
        ),
    ]