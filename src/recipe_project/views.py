from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

def login_view(request):
    error_message = None
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(
                username=username,
                password=password
            )

            if user is not None:
                login(request, user)
                return redirect('recipes:list')
            else:
                error_message = 'Invalid username or password. Please try again.'    
        else:
            error_message = 'Oops, something went wrong!'
    
    context = {
        'form': form,
        'error_message': error_message
    }

    return render(request, 'auth/login.html', context)

def logout_view(request):
    logout(request)
    return render(request, 'auth/success.html')

def signup_view(request):
    error_message = None
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('recipes:list')
        else:
            error_message = 'Please correct the errors below.'
        
    context = {
        'form': form,
        'error_message': error_message
    }

    return render(request, 'auth/signup.html', context)
