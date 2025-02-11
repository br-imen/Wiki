import random
import markdown2
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import EditEntryForm, NewEntryForm

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def title(request, title):
    found_content = util.get_entry(title)
    if found_content is None:
        return render(request, "encyclopedia/404.html", {"title": title}, status=404)
    else:
        html_content = markdown2.markdown(found_content)  # Convert Markdown to HTML
        return render(
            request, "encyclopedia/title.html", {"content": html_content, "title": title}
        )
    

def search(request):
    query = request.GET.get("q")
    result = []
    found_content =  util.get_entry(query.upper())
    if found_content:
        print(found_content)
        return render(
            request, "encyclopedia/title.html", {"content": found_content, "title": query}
        )
    else:
        entries = util.list_entries()
        result = [entry for entry in entries if query.lower() in entry.lower()] 
        return render(request,"encyclopedia/search_result.html", {"result":result,"input":query})


def create_entry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
        if util.get_entry(title):
            form.add_error("title", "An entry with this title already exists. Please choose another.")
            return render(request, "encyclopedia/create.html", {"form": form})
        util.save_entry(title,content)
        return redirect("title", title=title)
    else:
        form = NewEntryForm()
        return render(request, "encyclopedia/create.html", {"form": form})
    

def edit_entry(request, title):
    entry = util.get_entry(title)
    if request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid(): 
            updated_content = form.cleaned_data['content']
            util.save_entry(title, updated_content)
            return redirect('title', title=title)
    else:
        form = EditEntryForm(initial={'content':entry})
        return render(request, "encyclopedia/edit.html", {"form":form, "title": title})
    

def random_page(request):
    list_entries =  util.list_entries()
    if list_entries:
        random_title = random.choice(list_entries)
        return redirect('title', title=random_title)
    else:
        return HttpResponse("No entries available")