import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import camelot
from io import BytesIO
import base64
from PyPDF2 import PdfFileWriter, PdfFileReader


def parse_tables(file):
    try:
        tables = camelot.read_pdf(file, pages='all')
        print(tables)
        tables_images = [(table, table_image_b64(table)) for table in tables]
        return tables_images
    # file is not a pdf
    except NotImplementedError:
        return []


def in_page_range(file, page_range):
    pdf_file = PdfFileReader(file)
    num_pages = pdf_file.numPages
    return (0 < page_range[0] <= num_pages) and (0 < page_range[1] <= num_pages)


def table_image_b64(table):
    if table._image:
        image = table._image[0]
        coords_list = list(table._image[1].keys())
        coords_list.sort(key=lambda x: x[1])
        coords = coords_list[table.order - 1]
        plt.imshow(image[coords[3]:coords[1], coords[0]:coords[2]])
        plt.xticks([])
        plt.yticks([])
        buffer = BytesIO()
        plt.savefig(buffer, dpi=300, bbox_inches='tight')
        plt.close('all')
        return base64.encodebytes(buffer.getvalue()).decode()
    else:
        return ''


def cut_pdf(file, page_range):
    out = BytesIO()
    inputpdf = PdfFileReader(file)
    output = PdfFileWriter()
    for i in range(page_range[0] - 1, page_range[1]):
        output.addPage(inputpdf.getPage(i))
        output.write(out)
    return out
