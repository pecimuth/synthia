from marshmallow import Schema
from marshmallow.fields import Integer, Str, Nested


class MessageView(Schema):
    result = Str()
    message = Str()


class UserView(Schema):
    id = Integer()
    email = Str()


class UserAndTokenView(Schema):
    user = Nested(UserView())
    token = Str()
