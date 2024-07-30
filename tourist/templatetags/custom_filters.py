from django import template
from localguides.models import Guide

register = template.Library()

@register.filter(name='is_local_guide')
def is_local_guide(user):
    return not Guide.objects.filter(user=user).exists()
