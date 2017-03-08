from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from .forms import UserForm, AudioForm
from .models import User, Audio, Summary, Sentiment

from readless.Summarization import clusterrank
from speechmatics.individual import inditrans
from classifier import svm

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

def index(request):
	return render(request, "index.html")

def logout(request):
	if 'username' in request.COOKIES:
		context = {"msg" : "Logged Out"}
		response = redirect('/')
		response.delete_cookie('username')
		return response
	return HttpResponseRedirect('/')

def count_sentiment(obj, key, val):
	if key == 'food':
		obj.food_count += 1
		if val == 'good':
			obj.food_good_count += 1
		if val == 'bad':
			obj.food_bad_count += 1
		if val == 'neutral':
			obj.food_neutral_count += 1
	if key == 'ambience':
		obj.ambience_count += 1
		if val == 'good':
			obj.ambience_good_count += 1
		if val == 'bad':
			obj.ambience_bad_count += 1
		if val == 'neutral':
			obj.ambience_neutral_count += 1
	if key == 'service':
		obj.service_count += 1
		if val == 'good':
			obj.service_good_count += 1
		if val == 'bad':
			obj.service_bad_count += 1
		if val == 'neutral':
			obj.service_neutral_count += 1
	if key == 'cost':
		obj.cost_count += 1
		if val == 'good':
			obj.cost_good_count += 1
		if val == 'bad':
			obj.cost_bad_count += 1
		if val == 'neutral':
			obj.cost_neutral_count += 1

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
			user_object = User.objects.get(email = username)
			instance.email = user_object
			instance.save()
			audio_path=os.getcwd() + '/media/' + str(instance.name)
			api_id = '14800' #raw_input("Enter api user id for speechmatics :")
			api_token = 'MzgxNjc2NDQtNjZkOS00NjY2LTgxNzQtZWM3NGZjZDZkNWYy' #raw_input("Enter api token for speechmatics :")
			lang = "en-GB" #raw_input("Enter language code spoken(en-US/en-GB) :")
			os.system("mkdir " + os.getcwd() + '/media/' + username)
			# os.system("python " + os.getcwd()+ "/irapp/speechmatics/speechmatics.py -f " + audio_path + " -l " + lang + " -i " + api_id + " -t " + api_token + " -x -o " + os.getcwd() + "/media/" + username + '/' + str(instance.name)[6:-4] + '.txt')
			d = {}
			string = ''
			transcribed_path = os.getcwd() + "/media/" + username + '/' + str(instance.name)[6:-4] + '.txt'
			old_path = os.getcwd() + "/static/" + 'read.txt'
			new_path = os.getcwd() + "/static/" + 'abcd.txt'
			with open(old_path ,'r') as f:
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
			with open(new_path, 'w') as f:
				f.write(string + '\n.\n')
			clusterrank_obj = clusterrank.ClusterRank()
			summary = clusterrank_obj.summarizeFile(new_path)
			summary = summary[:summary.rfind('.') + 1]
			with open(transcribed_path, 'w') as f:
				f.write(summary)
			audio_object = Audio.objects.get(name=instance.name)
			summary_obj = Summary(name=username + '/' + str(instance.name)[6:-4] + '.txt', summaryId=audio_object)
			summary_obj.save()
			graph_obj = svm.Svm()
			details = graph_obj.call_multiple(d)
			try:
				sentiment_object = Sentiment.objects.get(sentimentId__email=user_object)
				print "bye"
			except Sentiment.DoesNotExist:
				print "hello"
				sentiment_object = Sentiment(sentimentId=audio_object)
			for i in details:
				for key, val in i.items():
					count_sentiment(sentiment_object, key, val)
			sentiment_object.save()
			csv_path = os.getcwd() + '/static' + '/data.csv'
			with open(csv_path , "w") as f:
				f.write("State,Postive,Neutral,Negative\n")
				if sentiment_object.ambience_count != 0:
					f.write("Ambience,%s,%s,%s\n"%((sentiment_object.ambience_good_count*100/sentiment_object.ambience_count),
													(sentiment_object.ambience_neutral_count*100/sentiment_object.ambience_count),
													(sentiment_object.ambience_bad_count*100/sentiment_object.ambience_count)))
				else:
					f.write("Ambience,%s,%s,%s\n"%(0, 0, 0))
				if sentiment_object.cost_count != 0:
					f.write("Cost,%s,%s,%s\n"%((sentiment_object.cost_good_count*100/sentiment_object.cost_count),
												(sentiment_object.cost_neutral_count*100/sentiment_object.cost_count),
												(sentiment_object.cost_bad_count*100/sentiment_object.cost_count)))
				else:
					f.write("Cost,%s,%s,%s\n"%(0, 0, 0))
				if sentiment_object.food_count != 0:
					f.write("Food,%s,%s,%s\n"%((sentiment_object.food_good_count*100/sentiment_object.food_count),
												(sentiment_object.food_neutral_count*100/sentiment_object.food_count),
												(sentiment_object.food_bad_count*100/sentiment_object.food_count)))
				else:
					f.write("Food,%s,%s,%s\n"%(0, 0, 0))
				if sentiment_object.service_count != 0:
					f.write("Service,%s,%s,%s\n"%((sentiment_object.service_good_count*100/sentiment_object.service_count),
													(sentiment_object.service_neutral_count*100/sentiment_object.service_count),
													(sentiment_object.service_bad_count*100/sentiment_object.service_count)))
				else:
					f.write("Service,%s,%s,%s\n"%(0, 0, 0))
			context = {"msg" : summary, "graph" : details}
			response = render(request, "graph.html", context)
			return response
		else:
			form = AudioForm()
			context = {"form" : form, "msg" : "Form not valid"}
			return render(request, "graph.html", context)
	else:
		form = AudioForm()
		context = {"form" : form}
		return render(request, "upload.html", context)