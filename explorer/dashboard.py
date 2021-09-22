import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
# import dpd_components as dpd
import numpy as np
import pandas as pd

from django_plotly_dash import DjangoDash
from search_utils import search as sr
from django.db.models import Count
from explorer.models import Document

category_frequencies = Document.objects.all().values_list('category__name').annotate(freq=Count("category__name"))
frequencies = {cat: count for cat, count in category_frequencies}

category_pie = go.Pie(labels=list(frequencies.keys()), values=list(frequencies.values()))
category_graph = dcc.Graph(id='category-graph', figure=dict(data=[category_pie], layout={'title': "Aandeel per categorie", "autosize": True}))

dashboard = DjangoDash(name='dashboard',
                       serve_locally=True,
                       )

categories = [{'label': cat, 'value': cat} for cat in frequencies.keys()]

dashboard.layout = html.Div(children=[
    html.H1(id='heading', children=["Documenten dashboard"]),
    html.Div(id='category-pie', children=[category_graph]),
    html.Hr(id='divider'),
    dcc.Dropdown(id='category-selector', options=categories, placeholder="Selecteer een categorie"),
    html.Div(id='dash-wordcloud'),
])



@dashboard.expanded_callback(
    dash.dependencies.Output('dash-wordcloud', 'children'),
    [dash.dependencies.Input('category-selector', 'value')]
)
def category_callback(category, *args, **kwargs):
    if category:
        documents = Document.objects.filter(category__name=category)
    else:
        documents = Document.objects.all()

    wc = sr.wordcloud_documents(documents)
    return [html.Img(src="data:image/png;base64," + wc, id='wordcloud-img', className='center')]
