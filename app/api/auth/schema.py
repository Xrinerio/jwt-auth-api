from marshmallow import Schema, fields


class SignUpSchema(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)


class LoginSchema(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)


class RefreshSchema(Schema):
    refresh_token = fields.String(required=True)
