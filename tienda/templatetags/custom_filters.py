from django import template

register = template.Library()

@register.filter
def formato_chileno(valor):
    try:
        valor = int(valor)
        return "${:,}".format(valor).replace(",", ".")
    except (ValueError, TypeError):
        return valor
