from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
<<<<<<< HEAD
from .forms import UploadFileForm
# from .models import User
=======
from .forms import UserForm, AudioForm
from .models import User, Audio
>>>>>>> jomy

def valid(file):
	print "\t\t\t\t\thiiiiiiiiiiiiiiiiiiiiiiiiiiiiii"
	if file.name[-4:] == ".mp3" :
		print "mp3"
	else:
		print "not mp3"

<<<<<<< HEAD
# Create your views here.
def upload(request):
    if request.method == 'POST':
    	print "Post : Upload"
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
        	valid(request.FILES['file'])
        else:
        	print "not valid"
        return HttpResponse("noooo")
        # return HttpResponseRedirect('/success')
    else:
        form = UploadFileForm()
        print "SADF"
    	return render(request, 'upload.html', {'form': form})
=======
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
			obj = User.objects.get(email = username)
			instance.email = obj
			instance.save()
############ Write a function for splitting audio here ###############
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
>>>>>>> jomy
