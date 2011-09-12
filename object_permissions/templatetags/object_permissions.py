from django import template
import re

register = template.Library()

@register.tag
def has_object_permission(parser, token):
    # uzycie - np. {% has_object_permission user project view as can_view_project %}

    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents.split()[0]

    # szukanie argumentow i slowa "as"
    m = re.search(r'(.*?) (.*?) (.*?) as (\w+)', arg)
    try:
        user_var, perm, object_var, result_name = m.groups()
    except ValueError:
        raise template.TemplateSyntaxError,\
        "Bad arguments in tag %r - usage: {% has_object_permission user object permission as variable_name %}" % tag_name

    return HasObjectPermissionNode(user_var, object_var, perm, result_name)

class HasObjectPermissionNode(template.Node):
    def __init__(self, user_var, object_var, perm, result_name):
        self.user_var = template.Variable(user_var)
        self.object_var = template.Variable(object_var)
        self.perm = perm
        self.result_name = result_name

    def render(self, context):
        user = self.user_var.resolve(context)
        object = self.object_var.resolve(context)
        context[self.result_name] = user.has_perm(self.perm, object)
        return ''

