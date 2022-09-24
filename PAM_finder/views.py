from django.shortcuts import render
from Bio import SeqIO
from io import StringIO
from PAM_finder import SearchingAlgorithm
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt, csrf_protect


@csrf_exempt
def index(request):
    return render(request, 'index.html')


@csrf_protect
def finder_tool(request):
    return render(request, 'finder_tool.html')


@csrf_exempt
def about_us(request):
    return render(request, 'about_us.html')


@csrf_protect
def result(request):
    if request.method == 'POST':
        file_text = request.POST['seqText']

        if not input_text:
            file_text = request.FILES['file']
            fasta_sequences = SeqIO.parse(StringIO(filename.read().decode()), str(filename).split(".")[-1])
            for fasta in fasta_sequences:
                name, file_text = fasta.id, str(fasta.seq)

        option_text = request.POST['cas']
        result_text = SearchingAlgorithm.search(file_text, option_text)

        return render(request, 'result.html')
