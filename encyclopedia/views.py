from django.shortcuts import render
from django import forms
from . import util
import random
from markdown2 import Markdown

markdowner = Markdown()

class TextForm(forms.Form):

    title =  forms.CharField(widget=forms.TextInput(attrs={'name':'title'}))

    content = forms.CharField(widget=forms.Textarea(attrs={'name':'content', 'rows':3, 'cols':5}))




def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, entry):
    #get a list of titles in lower case 
    entries = []
    for title in util.list_entries():
        entries.append(title.lower())  

    if entry.lower() in entries:
        content = markdowner.convert(util.get_entry(entry))
        return render(request,"encyclopedia/entry.html", {
            "entry": content,
            "entry_name": entry
        })
        
    else:
        return render(request,"encyclopedia/error.html")

def search_query(request):
    if request.method == "POST":
        query = request.POST['q']
        entries = util.list_entries()
        for title in entries:
            if query.lower() == title.lower():
                content = markdowner.convert(util.get_entry(query))
                return render(request,"encyclopedia/entry.html", {
                "entry": content,
                "entry_name": query
                })
            elif query.lower() in title.lower():
                suggestions = []
                suggestions.append(title)
                return render(request,"encyclopedia/suggestions.html", {
                "suggestions": suggestions,
                "entry_name": "Search Suggestions"
                })
        else:
            return render(request,"encyclopedia/error.html")
            
def create_page(request):
    if request.method == "POST":
        form = TextForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            entries = util.list_entries()           
            for entry in entries:
                if title.lower() == entry.lower():
                    return render(request,"encyclopedia/create_error.html")
            else:
                util.save_entry(title, content)
                content = markdowner.convert(util.get_entry(title))
                return render(request,"encyclopedia/entry.html", {
                "entry": content,
                "entry_name": title
                })
    return render(request,"encyclopedia/create_page.html",{
        "form" : TextForm()
        })

def edit_page(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]

    return render(request,"encyclopedia/edit_page.html",{
        "title" : title,
        "content" : content
        })

def save_edit(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        util.save_entry(title, content)
        content = markdowner.convert(util.get_entry(title))
    return render(request,"encyclopedia/entry.html", {
    "entry": content,
    "entry_name": title
    })

def random_page(request):
    entries = util.list_entries()
    random_num = random.randint(0,len(entries)-1)
    entry = entries[random_num]
    content = markdowner.convert(util.get_entry(entry))
    return render(request,"encyclopedia/entry.html", {
    "entry": content,
    "entry_name": entry
    })

