# encoding=utf-8

from django import forms
from tvenc.models import RecordedProgram


class GetNewJobForm(forms.Form):
    worker = forms.CharField(label="エンコーダ", max_length=100, required=True)
