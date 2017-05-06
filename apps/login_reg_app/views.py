from django.shortcuts import render, redirect
from .models import User
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .forms import RegisterForm, LoginForm
# Create your views here.
def signin(request):
    if 'user' in request.session:
        return redirect ('menu:index')
    else:
        regform = RegisterForm()
        logform= LoginForm()
        context = {
            "regForm": regform,
            "logForm": logform
         }
        return render(request, "login_reg_app/signin.html", context)

@require_http_methods(["POST"])
def to_register(request):
    response_from_model = User.objects.user_register(request.POST)
    print response_from_model
    if response_from_model[1] == False:
        for message in response_from_model[0]:
            messages.add_message(request, messages.INFO, message)
        return redirect('login:signin')
    else:
        if 'user' not in request.session:
            request.session['user'] = response_from_model[0].id
            request.session['username'] = response_from_model[0].username
        return redirect('menu:index')

@require_http_methods(["POST"])
def to_login(request):
    response_from_model = User.objects.user_login(request.POST)
    if not response_from_model[1]:
        for message in response_from_model[0]:
            messages.add_message(request, messages.INFO, message)
        return redirect('login:signin')
    else:
        if 'user' not in request.session:
            request.session['user'] = response_from_model[0].id
            request.session['username'] = response_from_model[0].username
        return redirect('menu:index')

def to_update(request, id):
    user = User.objects.get(id=id)
    if user.id == request.session['user']:
        response_from_model = User.objects.update_user(request.POST, user)
        if not response_from_model[1]:
            for message in response_from_model[0]:
                messages.add_message(request, messages.INFO, message)
    return redirect('menu:update_profile', id=user.id)


def update_password(request, id):
    User.objects.password_update(request.POST, id)
    return redirect('menu:update_profile')

def logout(request):
    request.session.clear()
    return redirect('menu:index')
