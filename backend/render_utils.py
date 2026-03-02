from jinja2 import Template
def render_report(html_template, data):
  with open(html_template) as file:
    template = Template(file.read())
    return template.render(data = data)