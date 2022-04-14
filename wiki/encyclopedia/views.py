from django.shortcuts import render
from django.http import HttpResponse
from . import util
from random import choice
from markdown2 import markdown

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, name):
    wiki = util.get_entry(name)    
    if(wiki == None):
        return render(request, "encyclopedia/error.html",{
            "wikiname": name
        })

    return render(request, "encyclopedia/wiki.html", {
        "wikiname": name,
        "wikicontent": markdown(wiki)
    })

def search(request):
    searchquery = request.POST["q"]

    wiki = util.get_entry(searchquery)    
    if(wiki != None):
        return render(request, "encyclopedia/wiki.html", {
            "wikiname": searchquery,
            "wikicontent": wiki
        })

    entries = util.list_entries()
    filteredentries = filter(lambda entry: searchquery in entry, entries)
    return render(request, "encyclopedia/index.html", {
        "entries": filteredentries
    })    

def random(request):
    entries = util.list_entries()
    entry = choice(entries)    

    return render(request, "encyclopedia/wiki.html", {
            "wikiname": entry,
            "wikicontent": util.get_entry(entry)
        })

def newpage(request):
    if request.method == 'POST':
        name = request.POST["name"]
        content = request.POST["content"]
        wiki = util.get_entry(name)    
        if(wiki != None):   
            return render(request, "encyclopedia/error.html",{
                "wikiname": name
            })
        else:
            util.save_entry(name, content)
            wiki = util.get_entry(name)
            return render(request, "encyclopedia/wiki.html", {
                "wikiname": name,
                "wikicontent": wiki
            })    

        
    return render(request, "encyclopedia/newpage.html")

def editpage(request, name):
    if request.method == 'POST':        
        content = request.POST["content"]
        util.save_entry(name, content)
        wiki = util.get_entry(name)
        return render(request, "encyclopedia/wiki.html", {
            "wikiname": name,
            "wikicontent": wiki
        })  

    wiki = util.get_entry(name)
    return render(request, "encyclopedia/editpage.html", {
        "wikiname": name,
        "wikicontent": wiki
    })