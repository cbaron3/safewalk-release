from marshmallow import Schema, fields, pre_load, validate, ValidationError

# Schema to validate Contact form data
class ContactSchema(Schema):
    name = fields.String(required=True)
    subject = fields.String(required=True)
    email = fields.String(required=True)
    message = fields.String(required=True)