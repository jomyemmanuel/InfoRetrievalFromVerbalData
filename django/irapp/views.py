from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .forms import UserForm, AudioForm
from .models import User, Audio, Summary, Sentiment

from readless.Summarization import clusterrank
from speechmatics.individual import inditrans
from classifier import svm

import subprocess
import os
import json
import nltk
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
			os.system("mkdir " + os.getcwd() + '/media/' + form.cleaned_data['email'])
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
		return HttpResponseRedirect('/upload')
	if request.method == 'POST':
		pas = request.POST['email'] + "|" + request.POST['password']
		a = User.objects.filter(email = request.POST['email'])
		b = User.objects.filter(password = pas)
		if len(set(a).intersection(b)) == 0:
			context = {"msg" : "Invalid User!!"}
			response = render(request, "login.html", context)
			return response		
		response = redirect('/dashboard')
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
	obj['%s_count'%key] += 1
	obj['%s_%s_count'%(key, val)] += 1
	return obj

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
			audio_path = os.getcwd() + '/media/' + str(instance.name)
			api_id = '19089' #raw_input("Enter api user id for speechmatics :")
			api_token = 'MmU0ZGQzMzEtZDQxZi00ZTNlLWFhZmUtMzMyODQ2NWZkMDk3' #raw_input("Enter api token for speechmatics :")
			lang = "en-GB" #raw_input("Enter language code spoken(en-US/en-GB) :")
			os.system("mkdir " + os.getcwd() + '/media/' + username + '/' + str(instance.name)[6:-4])
			os.system("python " + os.getcwd()+ "/irapp/speechmatics/speechmatics.py -f " + audio_path +
					 " -l " + lang + " -i " + api_id + " -t " + api_token + " -x -o " + os.getcwd() +
					  "/media/" + username + '/' + str(instance.name)[6:-4] + '/' + 'transcribed.txt')
			d = {}
			string = ''
			transcribed_path = os.getcwd()+"/media/"+'/'+username+'/'+str(instance.name)[6:-4]+'/'+'transcribed.txt'
			try:
				with open(transcribed_path ,'r') as f:
					for line in f:
						key = str(line.rstrip('\n'))
						line = f.next()
						if not line:
							break
						val = str(line.rstrip('\n'))
						if key not in d.keys():
							d[key] = val + " "
						else:
							d[key] += val + " "
			except IOError:
				response = render(request, "404.html")
				return response
			with open(transcribed_path, 'w') as f:
				for i, j in d.items():
					f.write(j + " ")
			tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
			fp = open(transcribed_path)
			data = fp.read()
			a = tokenizer.tokenize(data)
			with open(transcribed_path, 'w') as f:
				for i in a:
					f.write(i + '\n')
			clusterrank_obj = clusterrank.ClusterRank()
			summary = clusterrank_obj.summarizeFile(transcribed_path)
			summary = summary[:summary.rfind('.') + 1]
			with open(transcribed_path, 'w') as f:
				f.write(summary)
			audio_object = Audio.objects.get(name=instance.name)
			summary_obj = Summary(
				name=username+'/'+str(instance.name)[6:-4]+'/'+'transcribed.txt',
				summaryId=audio_object
			)
			summary_obj.save()
			graph_obj = svm.Svm()
			details = graph_obj.call_multiple(d)
			sentiment_object = Sentiment(
				name=username+'/'+str(instance.name)[6:-4]+'/'+'data.csv',
				sentimentId=audio_object
			)
			sentiment_object.save()
			sentiment_dict = {
				'ambience_count':0, 'ambience_good_count':0, 'ambience_neutral_count':0, 'ambience_bad_count':0,
				'cost_count':0, 'cost_good_count':0, 'cost_neutral_count':0, 'cost_bad_count':0,
				'food_count':0, 'food_good_count':0, 'food_neutral_count':0, 'food_bad_count':0,
				'service_count':0, 'service_good_count':0, 'service_neutral_count':0, 'service_bad_count':0
			}
			for i in details:
				for key, val in i.items():
					sentiment_dict = count_sentiment(sentiment_dict, key, val)
			csv_path = os.getcwd() + '/media/' + username + '/' + str(instance.name)[6:-4] + '/' + 'data.csv'
			with open(csv_path , "w") as f:
				f.write("State,Postive,Neutral,Negative\n")
				if sentiment_dict['ambience_count'] != 0:
					f.write("Ambience,%s,%s,%s\n"%(
						(sentiment_dict['ambience_good_count']*100/sentiment_dict['ambience_count']),
						(sentiment_dict['ambience_neutral_count']*100/sentiment_dict['ambience_count']),
						(sentiment_dict['ambience_bad_count']*100/sentiment_dict['ambience_count']))
					)
				else:
					f.write("Ambience,%s,%s,%s\n"%(0, 0, 0))
				if sentiment_dict['cost_count'] != 0:
					f.write("Cost,%s,%s,%s\n"%(
						(sentiment_dict['cost_good_count']*100/sentiment_dict['cost_count']),
						(sentiment_dict['cost_neutral_count']*100/sentiment_dict['cost_count']),
						(sentiment_dict['cost_bad_count']*100/sentiment_dict['cost_count']))
					)
				else:
					f.write("Cost,%s,%s,%s\n"%(0, 0, 0))
				if sentiment_dict['food_count'] != 0:
					f.write("Food,%s,%s,%s\n"%(
						(sentiment_dict['food_good_count']*100/sentiment_dict['food_count']),
						(sentiment_dict['food_neutral_count']*100/sentiment_dict['food_count']),
						(sentiment_dict['food_bad_count']*100/sentiment_dict['food_count']))
					)
				else:
					f.write("Food,%s,%s,%s\n"%(0, 0, 0))
				if sentiment_dict['service_count'] != 0:
					f.write("Service,%s,%s,%s\n"%(
						(sentiment_dict['service_good_count']*100/sentiment_dict['service_count']),
						(sentiment_dict['service_neutral_count']*100/sentiment_dict['service_count']),
						(sentiment_dict['service_bad_count']*100/sentiment_dict['service_count']))
					)
				else:
					f.write("Service,%s,%s,%s\n"%(0, 0, 0))
			context = {"summary" : summary, "path" : username+'/'+str(instance.name)[6:-4]}
			response = render(request, "graph.html", context)
			return response
		else:
			form = AudioForm()
			context = {"form" : form, "msg" : "Form not valid"}
			return render(request, "upload.html", context)
	else:
		form = AudioForm()
		context = {"form" : form}
		return render(request, "upload.html", context)

def dashboard(request):
	if 'username' in request.COOKIES:
		username = request.COOKIES['username']
	else:
		return HttpResponseRedirect('/login')
	if request.method == 'GET':
		audio_object = Audio.objects.filter(email=username).order_by('-timestamp')
		data = []
		index = 0
		for elm in audio_object:
			obj_list = []
			summary_obj = Summary.objects.filter(summaryId=elm)
			sentiment_obj = Sentiment.objects.filter(sentimentId=elm)
			obj_list.append(str(elm)[6:])
			if summary_obj and sentiment_obj:
				obj_list.append(summary_obj[0])
				obj_list.append(sentiment_obj[0])
				time = audio_object.values()[index]['timestamp']
				obj_list.append(time)
				data.append(obj_list)
			index += 1
		context = {'data' : data}
		return render(request, "dashboard.html", context)
	else:
		response = redirect('/')
		return response

@csrf_exempt
def summaryAPI(request):
	if request.method == 'POST':
		json_data = json.loads(request.body)
		resp = {'email':json_data['email'],'audio':json_data['audio']}
		try:
			req = User.objects.get(
				email=json_data['email'],
				password=json_data['email']+'|'+json_data['password']
			)
		except:
			resp['error_message'] = "Invalid User Credentials !"
			return HttpResponse(json.dumps(resp), content_type="application/json")
		try:
			aud = Audio.objects.get(email=req, name="audio/" + json_data['audio'])
			with open(os.getcwd()+'/media/'+json_data['email']+'/'+json_data['audio'][:-4]+'/'+'transcribed.txt', 'r') as f:
				string = f.read()
			resp['summary'] = string
		except:
			resp['error_message'] = "Audio File Not Found For User !"
			return HttpResponse(json.dumps(resp), content_type="application/json")
	return HttpResponse(json.dumps(resp), content_type="application/json")