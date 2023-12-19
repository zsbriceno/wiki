from django import forms

class NewEntryForm(forms.Form):
    entry = forms.CharField(label="New Entry", required=False)
    
class NewSearchForm(forms.Form):
    search = forms.CharField(label="Search", required=False)
    
