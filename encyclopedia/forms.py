from django import forms

class EntryForm(forms.Form):
    entry = forms.CharField(label="New Entry", required=False)
    
    
class SearchForm(forms.Form):
    search = forms.CharField(label="Search", required=False)
    
    
class CreateEntryForm(forms.Form):
    title = forms.CharField(label="Title", required=True)
    entry_content = forms.CharField(label="Entry", required=True, widget=forms.Textarea)
    

class EditEntryForm(forms.Form):
    content = forms.CharField(label="Content", required=True, widget=forms.Textarea, initial='')