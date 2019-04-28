from typing import Any, Dict

from cerealizer.fields.abstract import ValidatedField


def validate_cls_instance(cls_inst: Dict[str, ValidatedField], data: Dict, raise_exc: bool):
    validated_data, errors = {}, {}
    for k, v in cls_inst.items():
        try:
            val = v.validate(v, data.get(k))
            validated_data[k] = val
        except ValueError as e:
            if raise_exc:
                raise e
            errors[k] = str(e)
    return validated_data, errors


def is_serializer(key: str, value: Any):
    return isinstance(value, ValidatedField) and not key.startswith('_')


class DictSerializer:

    def __init__(self):
        self.validated_data = {}
        self.errors: Dict[str, str] = {}

    def validate(self, data: Dict, raise_exc=False):
        cls_inst = {key: value for (key, value) in self.__class__.__dict__.items()
                    if is_serializer(key, value)}
        self.validated_data, self.errors = validate_cls_instance(cls_inst, data, raise_exc)

    @property
    def is_valid(self) -> bool:
        if self.validated_data and not self.errors:
            return True
        return False


class AiohtttpRequestSerializer:

    def __init__(self):
        self.validated_data = {}
        self.errors: Dict[str, str] = {}

    async def validate(self, request, raise_exc=False):
        data = await request.json()
        cls_inst = {key: value for (key, value) in self.__class__.__dict__.items()
                    if is_serializer(key, value)}
        self.validated_data, self.errors = validate_cls_instance(cls_inst, data, raise_exc)