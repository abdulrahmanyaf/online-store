from django import template

register = template.Library()

class AddGetParameter(template.Node):
    def __init__(self, values):
        self.values = values

    def render(self, context):
        req = context.get("request")
        params = req.GET.copy()
        for key, value in self.values.items():
            params[key] = value.resolve(context)
        return "?{}".format(params.urlencode())

@register.tag
def add_get(parser, token):
    pairs = token.split_contents()[1:]
    values = {}
    for pair in pairs:
        s = pair.split("=", 1)
        values[s[0]] = parser.compile_filter(s[1])
    return AddGetParameter(values)
