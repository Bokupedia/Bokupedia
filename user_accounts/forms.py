from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from django import forms

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='Kullanıcı adı', max_length=150)
    first_name = forms.CharField(label='Ad', max_length=30, required=True)
    email = forms.EmailField(label='E-posta', required=True)
    password1 = forms.CharField(label='Parola', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Parola onayı', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Bu e-posta adresi zaten kayıtlı.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 8,
            'maxlength': 500,
            'class': 'bio-textarea'
        })
    )
    email = forms.EmailField(label='E-posta', required=False)

    class Meta:
        model = User
        fields = ['first_name', 'email', 'bio']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Bu e-posta adresi zaten kayıtlı.')
        return email