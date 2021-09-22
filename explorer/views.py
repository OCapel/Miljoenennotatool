from explorer.models import Document

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, reverse
from django.views import generic

from search_utils import search as sr

import json, urllib


def index(request):
    return render(request, 'explorer/index.html')


def search(request):
    if request.method == 'POST' and request.POST['search']:
        highlights, scores, wordcloud, category_frequencies, hl_terms = sr.search(request.POST['search'])

        return render(request, 'explorer/search_results.html',
                      {'highlights': highlights,
                       'term': request.POST['search'],
                       'scores': scores,
                       'wordcloud': wordcloud,
                       'category_frequencies': json.dumps(category_frequencies),
                       'hl_terms': urllib.parse.quote(hl_terms)}
        )
    else:
        return HttpResponseRedirect(reverse('explorer:index'))



def wordcloud(request):
    documents = Document.objects.filter(categorie='geo')
    wc = sr.wordcloud_documents(documents)
    return render(request, 'explorer/wordcloud.html',
                  {'wordcloud': wc}
                  )


def pdf_view(request, pk):
    document = Document.objects.get(pk=pk)
    with open(document.document.path, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=document.pdf'
        return response


def pdf_embedded(request, doc_id, terms):
    return render(request, 'explorer/pdf_view.html',
                  {
                      'doc_id': doc_id,
                      'terms': urllib.parse.unquote(terms)
                  })

# class DocumentView(generic.DetailView):
#     model = Document
#     template_name = 'explorer/document.html'
