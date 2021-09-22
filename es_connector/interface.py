import elasticsearch as es
from elasticsearch.helpers import streaming_bulk
from elasticsearch.exceptions import NotFoundError
import base64
from django.conf import settings

client = es.Elasticsearch()
index = settings.ELASTIC_INDEX


def documents(files):
    for doc_id, doc in files:
        yield {"document_id": doc_id,
               "document": base64.b64encode(doc).decode("ascii")}


def ingest_single_doc(doc_id, doc):
    for ok, result in streaming_bulk(
            client,
            documents([(doc_id, doc)]),
            index=index,
            doc_type="doc",
            chunk_size=1,
            params={"pipeline": "document_ingest"}
    ):
        action, result = result.popitem()
        if not ok:
            return False
        else:
            return result['_id']


def get_document(es_id):
    try:
        result = client.get(index=index, id=es_id, doc_type='doc')
        if 'content' in result['_source']['attachment']:
            return result['_source']['attachment']['content']
        else:
            return ''
    except NotFoundError:
        return False


def update_doc(es_id, new_values):
    try:
        result = client.update(index=index, id=es_id, doc_type='doc', body=new_values)
        return result
    except NotFoundError:
        return False


def delete_document(es_id):
    try:
        client.delete(index=index, id=es_id, doc_type='doc')
        return True
    except NotFoundError:
        return False
