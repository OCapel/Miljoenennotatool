import elasticsearch as es
from django.conf import settings


def run():
    client = es.Elasticsearch()
    index = settings.ELASTIC_INDEX
    client.ingest.put_pipeline(id='document_ingest', body={
        "description": "parse weerstand pdfs and index into ES",
        "processors":
            [
                {"attachment": {"field": "document"}},
                {"remove": {"field": "document"}}
            ]
    })


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

    client.indices.create(index=index, body=body)
