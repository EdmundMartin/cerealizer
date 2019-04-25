from typing import Dict, List

from cerealizer.fields.abstract import ValidatedField


class DictSerializer:

    def __init__(self):
        self.validated_data = {}
        self.errors: Dict[str, str] = {}

    def validate(self, data: Dict):
        for k, v in self.__class__.__dict__.items():
            if isinstance(v, ValidatedField):
                try:
                    val = v.validate(v, data.get(k))
                    self.validated_data[k] = val
                except ValueError as e:
                    self.errors[k] = str(e)

    @property
    def is_valid(self) -> bool:
        if self.validated_data and not self.errors:
            return True
        return False
