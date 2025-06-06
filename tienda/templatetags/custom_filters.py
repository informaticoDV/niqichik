from django import template
import urllib.parse

register = template.Library()

@register.filter
def formato_chileno(valor):
    try:
        valor = int(valor)
        return "${:,}".format(valor).replace(",", ".")
    except (ValueError, TypeError):
        return valor

@register.filter(name='add_class')
def add_class(field, css_class):
    existing_classes = field.field.widget.attrs.get('class', '')
    new_classes = f"{existing_classes} {css_class}".strip()
    return field.as_widget(attrs={"class": new_classes})

@register.filter
def urlquote(value):
    return urllib.parse.quote(str(value))
