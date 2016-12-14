from django import forms
from django.forms import ModelForm
from .models import User, Audio

class UserForm(ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	email =  forms.CharField(widget=forms.EmailInput)
	
	class Meta:
		model = User
		fields = '__all__'

class AudioForm(ModelForm):
	class Meta:
		model = Audio
		fields = ['name',]