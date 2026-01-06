"""
Forms for the accounts app.

Handles login and user-related form validation.
"""

from django import forms


class LoginForm(forms.Form):
    """
    Login form with username, password, and remember me option.
    
    The remember_me checkbox controls session duration:
    - Checked (default): 30-day session
    - Unchecked: Session expires on browser close
    """
    
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg '
                     'text-white placeholder-gray-400 focus:outline-none focus:border-primary-500 '
                     'focus:ring-1 focus:ring-primary-500 transition',
            'placeholder': 'Username',
            'autocomplete': 'username',
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg '
                     'text-white placeholder-gray-400 focus:outline-none focus:border-primary-500 '
                     'focus:ring-1 focus:ring-primary-500 transition',
            'placeholder': 'Password',
            'autocomplete': 'current-password',
        })
    )
    
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 rounded bg-white/5 border-white/20 text-primary-500 '
                     'focus:ring-primary-500 focus:ring-offset-0',
        })
    )
