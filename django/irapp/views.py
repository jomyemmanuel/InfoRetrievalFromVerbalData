from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .forms import UploadFileForm
# from .models import User

def valid(file):
	print "\t\t\t\t\thiiiiiiiiiiiiiiiiiiiiiiiiiiiiii"
	if file.name[-4:] == ".mp3" :
		print "mp3"
	else:
		print "not mp3"

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