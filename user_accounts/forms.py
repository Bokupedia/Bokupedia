from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from django import forms

class CustomUserCreationForm(UserCreationForm):
    
    first_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'password1', 'password2')
    
    def save(self, commit=True): 
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        if commit:
            user.save()
        return user
    
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'bio',]