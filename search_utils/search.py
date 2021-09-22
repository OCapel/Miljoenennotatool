import pandas as pd
# import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from wordcloud import WordCloud as wc

import elasticsearch as es
from elasticsearch_dsl import Search, Q
from functools import reduce

from django.conf import settings
from explorer.models import Document
from django.core.exceptions import ObjectDoesNotExist

index = settings.ELASTIC_INDEX
stop = set(stopwords.words('dutch'))
regex = re.compile(r'<em class="highlight">(.+?)</em>', re.IGNORECASE)
client = es.Elasticsearch()


def query(term, fragment_size=300):
    # q = Q("match_phrase", attachment__content={'query': term, 'slop': 0})
    q = create_query(term)
    s = Search(index=index).using(client) \
        .query(q) \
        .highlight('attachment.content', fragment_size=fragment_size, number_of_fragments=1000,
                   pre_tags='<em class="highlight">', post_tags='</em>')

    s = s[0:s.count()]

    return s.execute()


def or_ops(a, b):
    return a | b


def create_query(query):
    queries = []
    for term in query.split(' OR '):
        queries.append(Q("match_phrase", attachment__content={'query': term, 'slop': 0}))

    return reduce(or_ops, queries)


# if for some reason django db and es are not in sync, this function will return document if in django db, delete in es
# if not in django db
def get_or_delete(es_id):
    try:
        return Document.objects.get(es_id=es_id)
    except ObjectDoesNotExist:
        # delete
        return None


def get_highlights(response):
    docs_hits = [(get_or_delete(es_id=hit.meta.id), hit) for hit in response]
    return {doc: hit.meta.highlight.to_dict()['attachment.content'] for doc, hit in
            docs_hits if doc}, docs_hits


def get_relevance_timeseries(response):
    if len(response) > 1:
        date_scores = [(hit.attachment.date, hit.meta.score) for hit in response if 'date' in hit.attachment]
        score_series = pd.DataFrame(date_scores)
        score_series[0] = pd.to_datetime(score_series[0])
        score_series = score_series.set_index(0)
        grouped = score_series.groupby(pd.Grouper(freq='M')).mean().fillna(0)
        grouped.index = grouped.index.strftime('%Y-%m')
        return grouped.to_json()
    else:
        return {}


def get_wordcloud(highlights):
    if len(highlights.values()) > 0:
        words = ''
        for highlight in highlights.values():
            for sentence in highlight:
                words = words + sentence + ' '
        words = words.replace('<em class="highlight">', '')
        words = words.replace('</em>', '')
        list_of_words = [i.lower() for i in wordpunct_tokenize(words) if i.lower() not in stop and i.isalpha()]
        wordfreqdist = nltk.FreqDist(list_of_words)
        wordcloud = wc(max_font_size=100, background_color='white', width=1200, height=600).generate_from_frequencies(
            wordfreqdist)
        buffered = BytesIO()
        wordcloud.to_image().save(buffered, format="png")
        return base64.b64encode(buffered.getvalue()).decode('ascii')
    else:
        return ''


def wordcloud_documents(documents, width=1200, height=600):
    words = ''
    for document in documents:
        words += document.get_document()
    list_of_words = [i.lower() for i in wordpunct_tokenize(words) if i.lower() not in stop and i.isalpha()]
    wordfreqdist = nltk.FreqDist(list_of_words)
    wordcloud = wc(max_font_size=100, background_color='white', width=width, height=height).generate_from_frequencies(
        wordfreqdist)
    buffered = BytesIO()
    wordcloud.to_image().save(buffered, format="png")
    return base64.b64encode(buffered.getvalue()).decode('ascii')


# TODO leverage django queryset functionality
def disect_highlights(docs):
    frequencies = {}
    #frequencies = {'Overig': 0}
    terms = []
    for doc, hit in docs:
        freq = 0
        for hl in hit.meta.highlight['attachment.content']:
            highlighted = regex.findall(hl)
            freq += len(highlighted)
            terms += list(set(highlighted))
        if doc and doc.category:
            frequencies[doc.category.name] = freq
        else:
            pass
            #frequencies['Overig'] += freq
    return frequencies, ' '.join(list(set(terms)))


def search(term):
    response = query(term)

    highlights, doc_hits = get_highlights(response)

    category_counts, terms = disect_highlights(doc_hits)

    return highlights, get_relevance_timeseries(response), get_wordcloud(highlights), category_counts, terms
