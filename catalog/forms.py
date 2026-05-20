from django import forms

class TestForm(forms.Form):
    name = forms.CharField(max_length=100, label="Назва")
    description = forms.CharField(widget=forms.Textarea, label="Опис")