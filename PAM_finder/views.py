from django.shortcuts import render
from PAM_finder import SearchingAlgorithm
from django.core.files.storage import FileSystemStorage
from django.views.decorators import csrf_exempt


@csrf_exempt
def index(request):
    return render(request, 'index.html')


@csrf_exempt
def finder_tool(request):
    return render(request, 'finder_tool.html')


@csrf_exempt
def about_us(request):
    return render(request, 'about_us.html')


@csrf_exempt
def result(request):
    if request.method == 'POST':
        file_text = request.FILES['file']
        option_text = request.POST['cas']
        result_text = SearchingAlgorithm.search(file_text, option_text)

        return render(request, 'result.html')
