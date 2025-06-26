from django import template
import urllib.parse

register = template.Library()

@register.filter
def formato_chileno(valor):
    try:
        valor = float(valor)
        entero = int(valor)
        decimales = int(round((valor - entero) * 100))
        return "${:,}".format(entero).replace(",", ".") + (f",{decimales:02d}" if decimales else "")
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


@register.filter
def getitem(obj, key):
    try:
        return obj[key]  # esto sí funciona con forms
    except (KeyError, TypeError, AttributeError):
        return ''

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def attr(obj, attr_name):
    return getattr(obj, attr_name)

@register.filter
def to_range(start, end):
    try:
        start_int = int(start)
        end_int = int(end)
        return range(start_int, end_int + 1)
    except:
        return range(1)  # fallback vacío