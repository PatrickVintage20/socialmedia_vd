from django import forms

class VideoURLForm(forms.Form):
    url = forms.URLField(label='Video URL', required=True)
