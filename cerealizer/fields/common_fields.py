from typing import Union

from cerealizer.fields.abstract import ValidatedField
from cerealizer.validators.regex_validators import is_valid_url


class PositiveInteger(ValidatedField):

    def __init__(self, many=False):
        super().__init__()
        self.many = many

    def _validate_one(self, value):
        if not isinstance(value, int):
            raise ValueError('value must be an integer')
        if value <= 0:
            raise ValueError('value must be > 0')
        return value

    def validate(self, instance, value):
        if self.many:
            return self._validate_many(value)
        return self._validate_one(value)


class StringField(ValidatedField):

    def __init__(self, allow_none: bool=False, empty: bool=False, max_length: Union[None, int]=None,
                 many=False):
        super().__init__()
        self.allow_none = allow_none
        self.allow_empty = empty
        self.max_length = max_length
        self.many = many

    def _validate_one(self, value):
        if value is None and self.allow_none:
            return value
        if not isinstance(value, str):
            raise ValueError('value must be a string')
        if self.max_length and isinstance(self.max_length, int):
            if len(value) > self.max_length:
                raise ValueError('value must be shorter than {} chars'.format(self.max_length))
        return value

    def validate(self, instance, value):
        if self.many:
            return self._validate_many(value)
        return self._validate_one(value)


class URLField(ValidatedField):

    def __init__(self, allow_none: bool=False, empty: bool=False, many=False):
        super().__init__()
        self.allow_none = allow_none
        self.empty = empty
        self.many = many

    def _validate_one(self, value):
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

    def validate(self, instance, value):
        if self.many:
            return self._validate_many(value)
        return self._validate_one(value)
