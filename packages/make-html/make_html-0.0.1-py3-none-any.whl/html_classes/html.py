
try:
    from django.utils.safestring import mark_safe
except ImportError:
    mark_safe = lambda a: a


class HtmlElement:
    element = 'div'
    default_classes = []
    colour_class = ''
    default_colour = None

    def convert_kwargs(self):
        if self.colour:
            self.css_classes.append(self.colour_class + self.colour)
        kwarg_str = '' if not self.css_classes else f' class="{" ".join(self.css_classes)}"'
        for k, v in self.attributes.items():
            kwarg_str += f' {k.replace("_", "-")}="{v}"'
        return kwarg_str

    def tool_tip(self, tooltip):
        if tooltip:
            self.attributes.update({'data-tooltip': "tooltip", 'data-original-title': tooltip, 'data-html': 'true'})

    def __init__(self, contents=None, css_classes=None, element=None, tooltip=None, colour=None, **kwargs):
        if element:
            self.element = element
        self._contents = [contents] if contents else []
        self.attributes = kwargs
        self.tool_tip(tooltip)
        self.colour = colour if colour else self.default_colour
        if css_classes:
            self.css_classes = css_classes.split(' ') if type(css_classes) == str else css_classes.copy()
        else:
            self.css_classes = self.default_classes.copy()

    def get_contents(self):
        return ''.join([str(c) for c in self._contents])

    def render(self):
        return mark_safe(f'<{self.element}{self.convert_kwargs()}>{self.get_contents()}</{self.element}>')

    def append(self, html):
        self._contents.append(html)

    def add_class(self, classes):
        self.css_classes += classes.split(' ')

    def __str__(self):
        return self.render()

    @staticmethod
    def add_multiple_elements(data, element, **kwargs):
        elements = []
        for d in data:
            elements.append(HtmlElement(element=element, contents=str(d), **kwargs).render())
        return ''.join(elements)


class HtmlDiv(HtmlElement):
    pass


class HtmlTable(HtmlElement):

    element = 'table'

    def get_contents(self):
        fmt_items = []
        for i in self.rows[:self.headers]:
            fmt_items.append(self.add_multiple_elements(i, 'th', css_classes=self.header_classes))
        for r in self.rows[self.headers:]:
            fmt_items.append(self.add_multiple_elements(r[:self.left_headers], 'th', css_classes=self.header_classes))
            fmt_items.append(self.add_multiple_elements(r[self.left_headers:], 'td', css_classes=self.cell_classes))

        return self.add_multiple_elements(fmt_items, 'tr')

    def __init__(self, data=None, headers=0, left_headers=0, cell_classes=None, header_classes=None, row_classes=None,
                 **kwargs):
        super().__init__(**kwargs)
        self._data = data
        self.headers = headers
        self.left_headers = left_headers
        self.rows = [] if not data else [r for r in data]
        self.cell_classes = cell_classes
        self.header_classes = header_classes
        self.row_classes = row_classes
