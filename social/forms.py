from django import forms

class KeywordsForm(forms.Form):
    keyword = forms.CharField(label='Keyword', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    reddit = forms.BooleanField(label='Reddit', required=False, initial=True)
    twitter = forms.BooleanField(label='Twitter', required=False, initial=True)