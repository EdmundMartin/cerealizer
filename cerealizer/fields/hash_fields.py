from cerealizer.fields.abstract import ValidatedField
from cerealizer.validators.regex_validators import is_valid_sha1


class SHA1Field(ValidatedField):

    def __init__(self, required: bool = True, many: bool = False):
        super().__init__()
        self.required = required
        self.many = many

    def _validate_one(self, value):
        if len(value) == 40:
            raise ValueError('sha1 hash has wrong length: {}'.format(len(value)))
        return is_valid_sha1(value)

    def validate(self, instance, value):
        if self.many:
            return self._validate_many(value)
        return self._validate_one(value)