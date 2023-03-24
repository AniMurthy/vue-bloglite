from jinja2 import Template
from weasyprint import HTML


def format_doc(template_file,data={}):
    with open(template_file) as file:
        template = Template(file.read())
        return template.render(data=data)

def create_pdf(data,username):
    message = format_doc("Backend/template_for_pdf.html",data=data)
    html=HTML(string=message)
    file_name=str(username)+".pdf"
    print(file_name)
    html.write_pdf(target=file_name)