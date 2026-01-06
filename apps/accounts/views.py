"""
Authentication views for the accounts app.

Handles login, logout, and session management.
Sessions are configured for long duration (30 days) for mobile convenience.
"""

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import LoginForm


def login_view(request):
    """
    Handle user login.
    
    Displays login form and authenticates users.
    Redirects to 'next' parameter or calendar on success.
    """
    # If already logged in, redirect to calendar
    if request.user.is_authenticated:
        return redirect('planning:calendar')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me', True)
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                
                # If "remember me" is not checked, session expires on browser close
                if not remember_me:
                    request.session.set_expiry(0)
                
                messages.success(request, f'Welcome back, {user.display_name}!')
                
                # Redirect to next or calendar
                next_url = request.GET.get('next', 'planning:calendar')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """
    Handle user logout.
    
    Logs out the user and redirects to login page.
    """
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')
