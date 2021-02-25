from marshmallow import Schema, ValidationError
from marshmallow.fields import Integer, Str, Nested, List, Bool, Dict, Raw, Float
from marshmallow.validate import OneOf, Range

from core.service.column_generator import get_generator_by_name
from core.service.exception import SomeError


class MessageView(Schema):
    result = Str()
    message = Str()


class UserView(Schema):
    id = Integer()
    email = Str()


class UserAndTokenView(Schema):
    user = Nested(UserView())
    token = Str()
