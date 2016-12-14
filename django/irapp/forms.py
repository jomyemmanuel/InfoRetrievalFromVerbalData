from django import forms
from django.forms import ModelForm
from .models import User, Audio

class UserForm(ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
<<<<<<< HEAD
		fields = '__all__'
=======
		fields = '__all__'

class AudioForm(ModelForm):
	class Meta:
		model = Audio
		fields = ['name',]
>>>>>>> e122f79e93696d6790e1c4acfe7438e89a311eca
