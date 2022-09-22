from django.shortcuts import render
from PAM_finder import SearchingAlgorithm
from django.core.files.storage import FileSystemStorage


def index(request):
    return render(request, 'index.html')


def finder_tool(request):
    return render(request, 'finder_tool.html')


def about_us(request):
    return render(request, 'about_us.html')


def result(request):
    if request.method == 'POST':
        file_text = request.FILES['file']
        option_text = request.POST['cas']
        result_text = SearchingAlgorithm.search(file_text, option_text)
        print(option_text)

        context = {
            'seq_text': result_text
        }
        return render(request, 'result.html', context)
