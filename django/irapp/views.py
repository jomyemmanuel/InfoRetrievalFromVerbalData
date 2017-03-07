from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse,HttpResponseRedirect
from .forms import UserForm, AudioForm
from .models import User, Audio

from readless.Summarization import clusterrank
from speechmatics.individual import inditrans
from classifier import svm

from random import randint
from django.views.generic import TemplateView
# from chartjs.views.lines import BaseLineChartView

import subprocess
import os

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
			response = redirect('/upload')
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
		response = redirect('/upload')
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
			audio_path=os.getcwd()+'/media/'+str(instance.name)
			api_id = '14800' #raw_input("Enter api user id for speechmatics :")
			api_token = 'MzgxNjc2NDQtNjZkOS00NjY2LTgxNzQtZWM3NGZjZDZkNWYy' #raw_input("Enter api token for speechmatics :")
			lang = "en-GB" #raw_input("Enter language code spoken(en-US/en-GB) :")
			os.system("mkdir " + os.getcwd() + '/media/' + username)
			os.system("python " + os.getcwd()+ "/irapp/speechmatics/speechmatics.py -f " + audio_path + " -l " + lang + " -i " + api_id + " -t " + api_token + " -x -o " + os.getcwd() + "/media/" + username + '/' + str(instance.name)[6:-4] + '.txt')
			d = {}
			string=''
			transcribed_path = os.getcwd() + "/media/" + username + '/' + str(instance.name)[6:-4] + '.txt'
			with open(transcribed_path ,'r') as f:
				for line in f:
					key = str(line.rstrip('\n'))
					line = f.next()
					if not line:
						break
					val = str(line.rstrip('\n'))
					if key not in d.keys():
						d[key] = val
					else:
						d[key] += val
					string += val
			d['summary'] = string
			with open(transcribed_path, 'w') as f:
				f.write(string + '\n.\n')
			clusterrank_obj = clusterrank.ClusterRank()
			summary = clusterrank_obj.summarizeFile(transcribed_path)
			graph_obj = svm.Svm()
			graph_obj.call_multiple(d)
			details=graph_obj.total
			context = {"msg" : summary, "graph" : details}
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


def test_graph(request):
	return render(request, "test.html")

# class LineChartJSONView(BaseLineChartView):
#     def get_labels(self):
#         """Return 7 labels."""
#         return ["January", "February", "March", "April", "May", "June", "July"]

#     def get_data(self):
#         """Return 3 datasets to plot."""

#         return [[75, 44, 92, 11, 44, 95, 35],
#                 [41, 92, 18, 3, 73, 87, 92],
#                 [87, 21, 94, 3, 90, 13, 65]]


# line_chart = TemplateView.as_view(template_name='line_chart.html')
# line_chart_json = LineChartJSONView.as_view()
