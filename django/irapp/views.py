from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse,HttpResponseRedirect
from .forms import UserForm, AudioForm
from .models import User, Audio

import subprocess
import os
from diarization.diarizejruby import filter_parameters 
from splitting.split import split
from joining.joinscript import join
from speechmatics.individual import inditrans
# Create your views here.

def register(request):
	if 'username' in request.COOKIES:
		usernamejudge = request.COOKIES['username']
		return HttpResponseRedirect('/')
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
			context = {"msg" : "Welcome from Register!!", "token" : "loggedIn"}
			response = render(request, "index.html", context)
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
		context = {"msg" : "Welcome User from Login!!", "token" : "loggedIn"}
		response = render(request, "upload.html", context)
		response.set_cookie("username", a[0])
		return response
	else:
		return render(request, "login.html")

def home(request):
	return render(request, "home.html")

def index(request):
	return render(request, "index.html")

def logout(request):
	if 'username' in request.COOKIES:
		context = {"msg" : "Logged Out"}
		# response = render(request, "index.html", context)
		response = redirect('/')
		response.delete_cookie('username')
		return response
	return HttpResponseRedirect('/')

def upload(request):
	if 'username' in request.COOKIES:
		username = request.COOKIES['username']
	else:
		return HttpResponseRedirect('/login')
	if request.method == 'POST':
		form = AudioForm(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit = False)
			username = request.COOKIES['username']
			obj = User.objects.get(email = username)
			instance.email = obj
			instance.save()

############ Write a function for splitting audio here ###############
			audio_path=os.getcwd()+'/media/'+str(instance.name)
			#print str(instance.name)[6:-4]
			#audio_path='file://'+os.getcwd()+'/media/'+str(instance.name)
			#path_ruby=os.getcwd()+'/irapp/diarization/diarizejruby/hello.rb'
			#subprocess.call(['./irapp/diarization/diarizejruby/parse.sh',path_ruby,audio_path])
			api_id = raw_input("Enter api user id for speechmatics :")
			api_token = raw_input("Enter api token for speechmatics :")
			lang = raw_input("Enter language code spoken(en-US/en-GB) :")
			#d = filter_parameters.filterout(os.getcwd()+'/filtered.log')
			#base_dir = os.path.abspath(__file__ + "/../../")
			#listofspeakers=split(base_dir,d,username,str(instance.name))
			#inditrans(base_dir,d,username,str(instance.name),listofspeakers,api_id,api_token,lang)
			#join(base_dir,d,username,str(instance.name),listofspeakers)
			os.system("mkdir " + os.getcwd() + '/media/' + username)
			os.system("python " + os.getcwd()+ "/irapp/speechmatics/speechmatics.py -f " + audio_path + " -l " + lang + " -i " + api_id + " -t " + api_token + " -x -o " + os.getcwd() + "/media/" + username + '/' + str(instance.name)[6:-4] + '.txt')
			
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
