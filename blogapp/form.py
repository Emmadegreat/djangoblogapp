from django import forms
from blogapp.models import  BlogUser, ContactUs, NewsLetter
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib import messages
from django.core.exceptions import ValidationError

class RegisterForm(UserCreationForm):
    username = None
    email = forms.EmailField(label="Email", max_length=225, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="First Name", max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(label="Last Name", max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label="Password",max_length=20, widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label="Confirm Password", max_length=20, widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = BlogUser
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')


class LoginForm(forms.ModelForm):

    class Meta:
        model = BlogUser
        fields = ['email', 'password']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'Placeholder': 'Enter your email address'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'Placeholder': 'Enter your password'}),
        }

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']

            if not email or not password:
                raise ValidationError ("Please fill the blank spaces")

            if not authenticate(email=email, password=password):
                raise ValidationError('Invalid user credentials')

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['fullname', 'email', 'phone', 'message']
        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 5}),
        }


class SubscribeForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email address'
    }))


class UnSubscribeForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Subscribe to our newsletter'}))

