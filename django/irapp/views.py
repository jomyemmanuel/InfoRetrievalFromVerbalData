from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect

# Create your views here.
from .forms import UploadFileForm

def valid_audio(file):
	print file

	def upload(request):
		if request.method == 'POST':
			form = UploadFileForm(request.POST, request.FILES)
			if form.is_valid():
				if valid_audio(request.FILES['file']):
					pass
					return render(request,'upload.html',{'form': form})