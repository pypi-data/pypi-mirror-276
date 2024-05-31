# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DualInput(Component):
    """A DualInput component.


Keyword arguments:

- id (string; default 'dual_input'):
    The ID of the component.

- assistiveHintText (string; default 'Enter 3 or more characters for suggestions.'):
    The assistive hint text.

- govukHint (string; default 'For example WV1 4QR or Wolverhampton.'):
    The hint text below the main label.

- govukLabel (string; default 'Enter a postcode or local authority to see services provided in the area.'):
    The text for the main label.

- invalid (boolean; default False):
    Indicates whether the input is invalid.

- invalidText (string; default 'Please enter a valid postcode or local authority.'):
    The error text displayed when the input is invalid.

- label (string; default ''):
    The label for the input field.

- options (list; optional):
    The options for the suggestions.

- value (string; default ''):
    The value of the input field."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_oflog_components'
    _type = 'DualInput'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, label=Component.UNDEFINED, options=Component.UNDEFINED, value=Component.UNDEFINED, invalid=Component.UNDEFINED, govukLabel=Component.UNDEFINED, govukHint=Component.UNDEFINED, invalidText=Component.UNDEFINED, assistiveHintText=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'assistiveHintText', 'govukHint', 'govukLabel', 'invalid', 'invalidText', 'label', 'options', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'assistiveHintText', 'govukHint', 'govukLabel', 'invalid', 'invalidText', 'label', 'options', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(DualInput, self).__init__(**args)
