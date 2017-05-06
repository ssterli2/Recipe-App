from django.shortcuts import render, redirect
import requests
from django.views.decorators.http import require_http_methods
from .models import Recipe, Ingredient
from ..login_reg_app.models import User

# Create your views here.
def index(request):
    context = {}
    if 'user' in request.session:
        context["user"] = request.session["user"]
        return render(request, "menu_planning_app/index.html", context)
    else:
        return redirect('login:signin')

def search(request):
    context = {}
    if 'user' in request.session:
        context["user"] = request.session["user"]
        return render(request, "menu_planning_app/search.html", context)
    else:
        return redirect('login:signin')

@require_http_methods(['POST'])
def to_search(request, count):
    user = User.objects.get(id=request.session['user'])
    recipe_ids = []
    for recipe in user.recipes.all():
        recipe_ids.append(recipe.api_id.encode())
    count = int(request.POST['count'])
    search = request.POST['search']
    params = {'key': '99573a05929673d2d785adb1d0a695c0', 'q': search, "page" : count}
    r = requests.get('http://food2fork.com/api/search', params=params)
    print r.text
    context = {
        "results" : r.json(),
        "user" : user,
        "recipes" : recipe_ids,
        "next" : count+1,
        "previous" : count-1,
        "search" : search,
        "user" : request.session["user"]
    }
    return render(request, "menu_planning_app/search.html", context)

@require_http_methods(['POST'])
def favorite(request):
    user = User.objects.get(id=request.session['user'])
    Recipe.objects.new_recipe(request.POST, user)
    return redirect('menu:search')

@require_http_methods(['POST'])
def unfavorite(request):
    user = User.objects.get(id=request.session['user'])
    Recipe.objects.unfavorite(request.POST, user)
    return redirect('menu:search')

def profile(request, id):
    if 'user' in request.session and request.session['user'] == int(id):
        context = {
            "user" : User.objects.get(id=request.session['user']),
            "recipes" : Recipe.objects.all(),
            "ingredients": Ingredient.objects.all()
            }
        return render(request, "menu_planning_app/profile.html", context)
    else:
        return redirect('login:signin')

def update_profile(request, id):
    if 'user' in request.session and request.session['user'] == int(id):
        context = {
            "user" : User.objects.get(id=id),
            }
        return render(request, "login_reg_app/update_profile.html", context)
    else:
        return redirect('login:signin')


def recipe(request, id):
    context = {}
    if 'user' in request.session:
        context["recipe"] = Recipe.objects.get(id=id),
        context["user"] = request.session['user']
        return render(request, "menu_planning_app/recipe.html", context)
    else:
        return redirect('login:signin')
