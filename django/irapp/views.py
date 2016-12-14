from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .forms import UserForm, AudioForm
from .models import User, Audio


import os
from diarization.diarizejruby import filter_parameters 
from splitting.split import split
# Create your views here.

def register(request):
	if 'username' in request.COOKIES:
		usernamejudge = request.COOKIES['username']
		return HttpResponseRedirect('/home')
	if request.method == 'POST':
		a = User.objects.filter(email = request.POST['email'])
		if len(a) != 0:
			form = UserForm()
			context = {"form" : form, "msg" : "Email already registered"}
			return render(request, "signup.html", context)
		form = UserForm(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit = False)
			instance.password = form.cleaned_data['email'] + "|" + form.cleaned_data['password']
			instance.save()
			context = {"msg" : "Welcome from Register!!"}
			response = render(request, "home.html", context)
			response.set_cookie("username", form.cleaned_data['email'])
			return response
		else:
			form = UserForm()
			context = {"form" : form, "msg" : "Form not valid"}
			return render(request, "signup.html", context)
	else:
		form = UserForm()
		return render(request, "signup.html")

def login(request):
	if 'username' in request.COOKIES:
		username = request.COOKIES['username']
		return HttpResponseRedirect('/')
	if request.method == 'POST':
		pas = request.POST['email'] + "|" + request.POST['password']
		a = User.objects.filter(email = request.POST['email'])
		b = User.objects.filter(password = pas)
		if len(set(a).intersection(b)) == 0:
			context = {"msg" : "Invalid User!!"}
			response = render(request, "login.html", context)
			return response		
		context = {"msg" : "Welcome User from Login!!"}
		response = render(request, "home.html", context)
		response.set_cookie("username", a[0])
		return response
	else:
		return render(request, "login.html")

def home(request):
	return render(request, "home.html")

def logout(request):
	if 'username' in request.COOKIES:
		context = {"msg" : "Logged Out"}
		response = render(request, "home.html", context)
		response.delete_cookie('username')
		return response
	return HttpResponseRedirect('/home')

def upload(request):
	if 'username' in request.COOKIES:
		username = request.COOKIES['username']
	else:
		HttpResponseRedirect('/login')
	if request.method == 'POST':
		form = AudioForm(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit = False)
			username = request.COOKIES['username']
			obj = User.objects.get(email = username)
			instance.email = obj
			instance.save()
			filename = Audio.objects.select_related().filter(email=username).order_by('-id')[0]
		
############ Write a function for splitting audio here ###############
			d=filter_parameters.filterout(os.getcwd()+
				     '/irapp/diarization/diarizejruby/'+'filtered.log')
			base_dir=os.path.abspath(__file__ + "/../../")
			split(base_dir,d,username,str(filename))
			context = {"msg" : "Welcome from upload!!"}
			response = render(request, "home.html", context)
			return response
		else:
			form = AudioForm()
			context = {"form" : form, "msg" : "Form not valid"}
			return render(request, "upload.html", context)
	else:
		form = AudioForm()
		context = {"form" : form}
		return render(request, "upload.html", context)