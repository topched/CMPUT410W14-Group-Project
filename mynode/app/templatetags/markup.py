import markdown2
import re
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='convert_markdown')
@stringfilter
def convert_markdown(value):
    return mark_safe(markdown2.markdown(force_unicode(value),safe_mode=True))

@register.filter(name='sanitize_html')
@stringfilter
def sanitize_html(value):
    sanitizer = re.compile('<\/?(script|iframe)[^<]*>', re.I)
    return sanitizer.sub("", value)