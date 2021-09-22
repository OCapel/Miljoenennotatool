from django.db.models import Q, F, Value, Func
from explorer.models import Table

from functools import reduce


def or_ops(a, b):
    return a | b


def create_query(query):
    queries = []
    for term in query.split(' OR '):
        queries.append(Q(data__icontains=term))

    return reduce(or_ops, queries)

