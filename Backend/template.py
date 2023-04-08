from jinja2 import Template
from weasyprint import HTML
import os


def format_doc(template_file,data={}):
    with open(template_file) as file:
        template = Template(file.read())
        return template.render(data=data)

def create_pdf(data,username):
    if not os.path.exists('../data'):
        os.makedirs('../data')
    message = format_doc("template_for_pdf.html",data=data)
    html=HTML(string=message)
    file_name=str("../data/"+username)+".pdf"
    html.write_pdf(target=file_name)