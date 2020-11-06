from django import forms
from django.db import transaction

from announcement.models import AnnouncementDocument


class DocumentUploadForm(forms.ModelForm):
    name = forms.CharField(label='Наименование документа', max_length=255)
    description = forms.CharField(label='Описание', widget=forms.Textarea(attrs={'class': 'form-control'}),
                                  required=False)
    file = forms.FileField(label='Файл', widget=forms.widgets.FileInput())
    student = forms.HiddenInput

    class Meta:
        model = AnnouncementDocument
        fields = ('name', 'description', 'file',)

    @transaction.atomic
    def save(self):
        announcement_document = AnnouncementDocument.objects.create(name=self.cleaned_data.get('name'),
                                                                    description=self.cleaned_data.get('description'),
                                                                    file=self.cleaned_data.get('file'),
                                                                    announcement=self.announcement)
