import os

from django.core.files.uploadedfile import SimpleUploadedFile

from explorer.models import Document


def run():
    folder = 'data/'
    extensions = ('.doc', '.docx', '.pdf', '.xls', '.xlsx', '.txt', '.ppt', '.pptx')
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(extensions):
                with open(os.path.join(root, file), 'rb') as f:
                    d = Document(title=file, document=SimpleUploadedFile(file, f.read()))
                    d.save()
