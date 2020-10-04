from django import forms

class SearchForm(form.forms):
	tweet_search = forms.CharField(label = 'Type the word or phrase that you want to analyze ', max_length = 50)