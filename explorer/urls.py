from django.urls import path
from django.views.generic import TemplateView
from . import views
try:
  from explorer import dashboard
except ImportError:
  pass

app_name = 'explorer'
urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('document/<int:pk>', views.pdf_view, name='document'),
    path('wordcloud', views.wordcloud),
    path('pdf_embedded/<int:doc_id>/<str:terms>', views.pdf_embedded, name='embedded'),
    path('dashboard', TemplateView.as_view(template_name='explorer/dashboard.html'))
]