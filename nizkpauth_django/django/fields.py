from typing import Any

from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from nizkpauth.profiles import Profile
from nizkpauth.utils import decode_string, encode_string


class NIZKPProfileField(models.Field):
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 200
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return Profile.import_json(decode_string(value))

    def to_python(self, value: Any) -> Any:
        if isinstance(value, Profile):
            return value
        
        if value is None:
            return value

        return Profile.import_json(decode_string(value))
    
    def get_prep_value(self, value: Any) -> Any:
        return encode_string(value.export_json())
    
    def get_internal_type(self):
        return "CharField"
