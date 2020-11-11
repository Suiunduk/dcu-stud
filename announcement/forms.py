from django import forms
from django.db import transaction

from announcement.models import AnnouncementDocument, AnnouncementAdditionalDocumentNames, AnnouncementApplicants


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


class AdditionalDocumentCreateForm(forms.ModelForm):
    name = forms.CharField(label='Наименование документа', max_length=255)
    description = forms.CharField(label='Краткое описание', widget=forms.Textarea(attrs={'class': 'form-control'}),
                                  required=False)
    announcement = forms.HiddenInput

    class Meta:
        model = AnnouncementAdditionalDocumentNames
        fields = ('name', 'description',)

    @transaction.atomic
    def save(self):
        announcement_document_name = AnnouncementAdditionalDocumentNames.objects.create(
            name=self.cleaned_data.get('name'),
            description=self.cleaned_data.get('description'),
            announcement=self.announcement)


class RejectForm(forms.Form):
    rejection_reason = forms.CharField(label='Причина отказа', widget=forms.Textarea(attrs={'class': 'form-control'}))
