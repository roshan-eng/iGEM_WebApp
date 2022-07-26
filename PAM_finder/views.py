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
        file_text = str(file_text).replace("\n", "")
        file_text = str(file_text).replace("\r", "")

        if not file_text:
            file_text = request.FILES['file']
            fasta_sequences = SeqIO.parse(StringIO(file_text.read().decode()), str(file_text).split(".")[-1])
            for fasta in fasta_sequences:
                name, file_text = fasta.id, str(fasta.seq)

        option_text = request.POST['pam']
        drop_option = False
        if not option_text:
            option_text = request.POST['cas']
            drop_option = True

        result_text = SearchingAlgorithm.search(file_text, option_text, drop_option)

        return render(request, 'result.html')
