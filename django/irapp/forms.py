from django import forms
from django.forms import ModelForm
<<<<<<< HEAD
# from .models import user
=======
from .models import User, Audio
>>>>>>> jomy

class UploadFileForm(forms.Form):
    file = forms.FileField()
    
# class UserForm(ModelForm):
# 	password = forms.CharField(widget=forms.PasswordInput)

<<<<<<< HEAD
# 	class Meta:
# 		model = User
# 		fields = '__all__'
=======
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
>>>>>>> jomy
