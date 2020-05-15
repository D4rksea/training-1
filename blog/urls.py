from django.urls import path
from . import views
from .views import listaPostView, PostDetailView2, modificaPostView, eliminaPostView

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('lista-post', listaPostView.as_view(), name='lista_post'),
    path('leggi-post/<int:pk>', PostDetailView2, name='leggi_post'),
    path('modifica-post/<int:pk>', modificaPostView, name='modifica_post'),
    path('elimina-post/<int:pk>', eliminaPostView, name='elimina_post'),
    path('crea-post', views.creaPostView, name='crea_post'),
]