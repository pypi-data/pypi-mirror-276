from django.template import (
    library,
    Template,
    Context,
)

register = library.Library()

@register.filter(name="render_to_string")
def meta_tags(content, context):
    template = Template(content)
    return template.render(Context(context))
