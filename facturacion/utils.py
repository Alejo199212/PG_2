from io import BytesIO
from xhtml2pdf import pisa
import base64
from django.http import HttpResponse
from django.template.loader import get_template

def renderPDF(template_src,contexto={}):
    template = get_template(template_src)
    html = template.render(contexto)
    
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), dest=None)
    pdfBase64 = base64.b64encode(pdf.dest.getvalue()).decode('utf-8')
    if not pdf.err:
        return pdfBase64
    return None

