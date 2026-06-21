from django import template

register = template.Library()


class CaptureNode(template.Node):
    def __init__(self, nodelist, varname):
        self.nodelist = nodelist
        self.varname = varname

    def render(self, context):
        # Render everything inside the block into a string
        output = self.nodelist.render(context)
        # Save that string into the template context variable name provided
        context[self.varname] = output
        return ""


@register.filter
def get_attr(obj, attr_name):
    return getattr(obj, attr_name, None)


@register.filter
def has_attr(obj, attr_name):
    return hasattr(obj, attr_name)


@register.filter
def split(value, key):
    return value.split(key)


@register.tag(name="capture")
def do_capture(parser, token):
    """
    Captures the contents of a template block and saves it into a variable.
    Usage: {% capture as my_variable %} ... HTML Content ... {% endcapture %}
    """
    bits = token.split_contents()
    if len(bits) != 3 or bits[1] != "as":
        raise template.TemplateSyntaxError(
            "'capture' node requires 'as variable' format"
        )

    varname = bits[2]
    # Parse everything up until the {% endcapture %} tag
    nodelist = parser.parse(("endcapture",))
    parser.delete_first_token()
    return CaptureNode(nodelist, varname)
