from django.db import models


class SeqModel(models.Model):
    title = models.CharField(max_length=80)
    pdf = models.FileField(upload_to='Sequences/')

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f"{self.title}"
