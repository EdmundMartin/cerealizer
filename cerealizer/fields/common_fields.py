from typing import Union

from cerealizer.fields.abstract import ValidatedField
from cerealizer.validators.regex_validators import is_valid_url


class PositiveInteger(ValidatedField):

    def validate(self, instance, value):
        if not isinstance(value, int):
            raise ValueError('value must be an integer')
        if value <= 0:
            raise ValueError('value must be > 0')
        return value


class StringField(ValidatedField):

    def __init__(self, allow_none: bool=False, empty: bool=False, max_length: Union[None, int]=None):
        super().__init__()
        self.allow_none = allow_none
        self.allow_empty = empty
        self.max_length = max_length

    def validate(self, instance, value):
        if value is None and self.allow_none:
            return value
        if not isinstance(value, str):
            raise ValueError('value must be a string')
        if self.max_length and isinstance(self.max_length, int):
            if len(value) > self.max_length:
                raise ValueError('value must be shorter than {} chars'.format(self.max_length))
        return value


class URLField(ValidatedField):

    def __init__(self, allow_none: bool=False, empty: bool=False):
        super().__init__()
        self.allow_none = allow_none
        self.empty = empty

    def validate(self, instance, value):
        if self.allow_none and value is None:
            return value
        if self.empty and value == '':
            return value
        if not isinstance(value, str):
            raise ValueError('a url must be string')
        valid_url = is_valid_url(value)
        if not valid_url:
            raise ValueError('invalid url: {}'.format(value))
        return value


class ManyField(ValidatedField):

    def __init__(self, field):
        super().__init__()
        self.field = field()

    def validate(self, instance, value):
        vals = []
        for i in value:
            vals.append(self.field.validate(instance, i))
        return vals