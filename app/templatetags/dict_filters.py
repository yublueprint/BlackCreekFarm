import qrcode
import io
import base64
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

@register.simple_tag
def generate_raw_qr(category, obj_id):
    # Construct the raw data string, e.g., "Supplies:4"
    raw_data = f"{category}:{obj_id}"
    
    # Generate the QR Code
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(raw_data)
    qr.make(fit=True)
    
    # Save to an in-memory buffer
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    
    # Encode to base64 string
    qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{qr_base64}"