from abstra_internals.widgets.widget_base import Input


class TextInput(Input):
    type = 'text-input'
    empty_value = ''

    def __init__(self, key: str, label: str, **kwargs):
        super().__init__(key)
        self.set_props(dict(label=label, **kwargs))

    def set_props(self, props):
        self.label = props.get('label', '')
        self.required = props.get('required', True)
        self.value = props.get('initial_value', self.empty_value)
        self.placeholder = props.get('placeholder', '')
        self.hint = props.get('hint', None)
        self.full_width = props.get('full_width', False)
        self.mask = props.get('mask', None)
        self.disabled = props.get('disabled', False)

    def render(self, ctx: dict):
        return {'type': self.type, 'key': self.key, 'label': self.label,
            'value': self.serialize_value(), 'placeholder': self.
            placeholder, 'required': self.required, 'hint': self.hint,
            'fullWidth': self.full_width, 'mask': self.mask, 'disabled':
            self.disabled, 'errors': self.errors}

    def serialize_value(self) ->str:
        return self.value or ''
