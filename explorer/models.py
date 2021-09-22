from django.db import models
from es_connector import interface as es
import pandas as pd
from django.db.models.signals import post_save
from django.dispatch import receiver
from document_parser import pdf


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


# Create your models here.
class Document(models.Model):
    title = models.CharField(max_length=1000)
    document = models.FileField(default=None)
    es_id = models.CharField(max_length=1000)
    category = models.ForeignKey('explorer.Category', default=2, on_delete=models.SET_DEFAULT)

    def index_document(self):
        if self.document and not self.es_id:
            result = es.ingest_single_doc(self.id, self.document.file.file.read())
            if result:
                self.es_id = result

    def get_document(self):
        return es.get_document(self.es_id)

    def delete_document(self):
        if self.es_id:
            if es.delete_document(self.es_id):
                self.es_id = ''

    def save_tables(self, tables):
        for table, img in tables:
            t = Table(data=table.df.to_json(), img=img, document=self)
            t.save()

    def save(self, *args, **kwargs):
        self.index_document()
        super(Document, self).save(*args, **kwargs)
        #tables = pdf.parse_tables(self.document.path)
        #self.save_tables(tables)

    def delete(self, *args, **kwargs):
        self.delete_document()
        super(Document, self).delete(*args, **kwargs)

    def __str__(self):
        return self.title


@receiver(models.signals.post_delete, sender=Document)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Document` object is deleted.
    """
    instance.delete_document()
    if instance.document:
        instance.document.delete(save=False)


class Table(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    data = models.TextField(default='')
    img = models.TextField(default='')

    def to_html(self):
        # TODO replace before putting data in db
        df = pd.read_json(self.data.replace('-\\n', '').replace('\\n', ' ')).sort_index()
        return df.to_html(classes=['table'], escape=False)

    @property
    def table_len(self):
        return len(self.data)

    def __str__(self):
        return '{}, {}'.format(self.id, self.document)
