from django.shortcuts import render
from django.http import HttpResponse
from polls.FileUploadForm import FileUploadForm
from django.conf import settings

# Create your views here.
def index(request):
    form = FileUploadForm
    return render(request, 'index.html',{'form':form})

def upload_file(request):
    if request.method == 'POST':
        path = settings.STATICFILES_DIRS
        print(path)
        if request.is_ajax():
            message = "Yes, AJAX!"

    return HttpResponse(message)
