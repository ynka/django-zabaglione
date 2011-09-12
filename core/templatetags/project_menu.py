# -*- coding: utf-8 -*-

from django import template
from core.models import Project
register = template.Library()

@register.inclusion_tag('core/_project_menu.html')
def project_menu(project, user):
    return {'project':project, 'user':user}
