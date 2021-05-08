from marshmallow import Schema
from marshmallow.fields import Int, Str, Nested


class MessageView(Schema):
    result = Str()
    message = Str()


class UserView(Schema):
    id = Int()
    email = Str()


class UserWrite(Schema):
    email = Str()
    pwd = Str()


class UserAndTokenView(Schema):
    user = Nested(UserView())
    token = Str()
