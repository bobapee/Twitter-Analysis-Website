from django import forms

class SearchForm(forms.Form):
	tweet_search = forms.CharField(max_length = 50, widget = forms.TextInput(attrs={'placeholder' : 'Word or Tweet here...'}))
