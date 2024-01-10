from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from markdown2 import Markdown
from . import util
from . import forms
import random


def index(request):
    entries = util.list_entries()
    
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })
    

def entry(request, title):
    content = html_conversion(title)

    if content is None:
        return render(request, "encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": content
        })
        
        
def search(request):
    entries = util.list_entries()
    title = request.GET.get('q', '')
    content = html_conversion(title)
    
    if content is None:
        results = []
        
        for entry in entries:
            if title.lower() in entry.lower():
                results.append(entry)
        
        if not results:
            return render(request, "encyclopedia/error.html", {
                "error_message": "This entry was not found."
            })
        else:
            return render(request, "encyclopedia/results.html", {
                "results": results
            })
    else:
        return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": content
            })
        

def new_entry(request):
    if request.method == "POST":
        form = forms.CreateEntryForm(request.POST)
        
        if form.is_valid():
            title = form.cleaned_data["title"]
            entry_content = form.cleaned_data["entry_content"]
            
            content_check = util.get_entry(title)
            
            if content_check is not None:
                return render(request, "encyclopedia/error.html", {
                    "error_message": "This entry already exists"
                })
            else:
                util.save_entry(title, entry_content)
                
                content = html_conversion(title)
                
                return render(request, "encyclopedia/entry.html", {
                    "title": title,
                    "content": content
                })
        
        
    return render(request, "encyclopedia/new_entry.html", {
        "form": forms.CreateEntryForm()
    })
    
    
def edit_entry(request, title):
    content = util.get_entry(title)
    
    if content is None:
        return render(request, "encyclopedia/error.html", {
                "error_message": "This entry does not exist."
            })
    else:
        if request.method == "GET":
            form = forms.EditEntryForm()
            form.fields["content"].initial = content
            
            return render(request, "encyclopedia/edit_entry.html", {
                "title": title,
                "form": form
        })
        elif request.method == "POST":
            form = forms.EditEntryForm(request.POST)
            if form.is_valid():
                new_content = form.cleaned_data["content"]
                util.save_entry(title, new_content)
                new_html_content = html_conversion(title)
                return render(request, "encyclopedia/entry.html", {
                    "title": title,
                    "content": new_html_content
                })
            else:
                return render(request, "encyclopedia/error.html", {
                "error_message": "Invalid form data."
            })
                
                
def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    random_content = html_conversion(random_entry)
    
    return HttpResponseRedirect(reverse("entry", kwargs={"title": random_entry}))
        

def html_conversion(entry_name):
    markdowner = Markdown()
    entry = util.get_entry(entry_name)
    html_entry = markdowner.convert(entry) if entry else None
    return html_entry
    