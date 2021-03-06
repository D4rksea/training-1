from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import BlogPostModelForm
from .models import BlogPostModel
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
def index(request): 
    command_list = ['crea-post','lista-post']
    context = {
        'command_list': command_list,
    }
    return render(request, "blog/index.html", context)

class listaPostView(ListView):
    model = BlogPostModel #modello dei dati da utilizzare 
    template_name = "blog/lista_post.html"  #pagina per mostrare i dati
    
    #recupera di dati da passare alla pagina per il render
    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context["posts"] = BlogPostModel.objects.all()
    #    return context

class PostDetailView(DetailView):
    model = BlogPostModel #modello dei dati da utilizzare 
    template_name = "blog/post_detail.html" #pagina per mostrare i dati

#Modifica del post
def modificaPostView(request, pk=None):
    obj = get_object_or_404(BlogPostModel, pk=pk) #carico il post in base alla chiave primaria pk
    form = BlogPostModelForm(request.POST or None, instance=obj)  #passo l'oggetto post al form
    if request.method == 'POST': 
        if form.is_valid():
           form.save()
           return redirect('/blog/lista-post')
    context = {"form": form,"pk":pk} #creo i parametri
    return render(request, 'blog/modifica_post.html', context)

def eliminaPostView(request, pk=None):
    obj = get_object_or_404(BlogPostModel, pk=pk) #carico il post in base alla chiave primaria pk
    obj.delete()
    return HttpResponseRedirect("blog/lista-post")

@login_required(login_url='/accounts/login/')
#Creazione del post
def creaPostView(request):
    if request.method == "POST": 
        form = BlogPostModelForm(request.POST) #ottengo il form dalla richiesta
        if form.is_valid():     #validazione del form
            print("Il Form è Valido!")
            new_post = form.save(commit=False)  #creo il post ma non lo salva
            new_post.autore=request.user
            new_post.save()
            print("new_post: ", new_post)
            return HttpResponseRedirect("lista-post")
    else: #se la chiamata non è POST vuol dire che è la prima chiamata GET, quindi mostro il form vuoto
        form = BlogPostModelForm()
    context = {"form": form}   #contesto dei parametri da passare al render
    return render(request, "blog/crea_post.html", context)  #passo il form alla pagina per il render

# # Creazione del commento
# @login_required(login_url='/accounts/login/')
# def creaCommentView(request, pk):
#     post = get_object_or_404(BlogPostModelForm, pk=pk)
#     if request.method == "POST":
#         form = BlogCommentModelForm(request.POST)  # ottengo il form dalla richiesta
#         if form.is_valid():  # validazione del form
#             print("Il Form è Valido!")
#             new_comment = form.save(commit=False)  # creo il post ma non salvo
#             new_comment.post = post
#             new_comment.autore = request.user
#             print("new_comment: ", new_comment)
#             new_comment.save()
#             url_discussione = reverse("risposte_post", kwargs={"pk": pk})
#             return HttpResponseRedirect(url_discussione)
#     else:  # se la chiamata non è POST vuol dire che è la prima chiamata GET, quindi mostro il form vuoto
#         form = BlogCommentModelForm()
#     context = {"form": form}  # contesto dei parametri da passare al render
#     return render(request, "blog/crea_comment.html", context)  # passo il form alla pagina per il render