from django import forms
from django.forms import ModelForm
# from .models import User

# class UserForm(ModelForm):
# 	password = forms.CharField(widget=forms.PasswordInput)
# from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
	# class Meta:
	# 	model = User
	# 	fields = '__all__'
