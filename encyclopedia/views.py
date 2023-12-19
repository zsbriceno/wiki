from django.shortcuts import render
from markdown2 import Markdown
from . import util
from . import forms

entries = util.list_entries()

def index(request):
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
    title = request.GET.get('q', '')
    content = html_conversion(title)
    
    if content is None:
        results = []
        
        for entry in entries:
            if title.lower() in entry.lower():
                results.append(entry)
        
        if not results:
            return render(request, "encyclopedia/error.html")
        else:
            return render(request, "encyclopedia/results.html", {
                "results": results
            })
    else:
        return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": content
            })


def html_conversion(entry_name):
    markdowner = Markdown()
    entry = util.get_entry(entry_name)
    html_entry = markdowner.convert(entry) if entry else None
    return html_entry
    