from django import forms
from django.forms import ModelForm
from .models import User

class UserForm(ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = '__all__'
