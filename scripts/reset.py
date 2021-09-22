from explorer.models import Document

import elasticsearch as es
from django.conf import settings


def run():
    # clear document table (django)
    print("Clearing document table")
    docs = Document.objects.all()
    docs.delete()

    # clear elasticsearch index
    client = es.Elasticsearch()
    index = settings.ELASTIC_INDEX
    body = {'settings': {'analysis': {'analyzer': {'my_analyzer': {'type': 'custom',
                                                               'filter': ['lowercase', 'my_snow'],
                                                               "char_filter": [
                                                                   "my_char_filter"
                                                               ],
                                                               'tokenizer': 'standard'}},
                                  'filter': {'my_stemmer': {'name': 'dutch',
                                                            'type': 'stemmer'},
                                             'my_stemmer2': {'name': 'possessive_english',
                                                             'type': 'stemmer'},
                                             'my_snow': {'type': 'snowball',
                                                         'language': 'dutch'}},
                                  'char_filter': {'my_char_filter': {"type": "mapping",
                                                                     "mappings": [
                                                                         "’ => '",
                                                                         "` => '"
                                                                     ]}}}},
        'mappings': {'doc': {'properties': {'attachment.content': {'type': 'text', 'analyzer': 'my_analyzer'}}}}
        }

    print("Resetting elasticsearch index")
    client.indices.delete(index=index)
    print('Recreate indices')
    client.indices.create(index=index, body=body)