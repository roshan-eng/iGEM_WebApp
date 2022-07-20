from django import forms
from .models import SeqModel


class UploadSeqForm(forms.ModelForm):
    class Meta:
        model = SeqModel
        fields = ('title', 'pdf',)
