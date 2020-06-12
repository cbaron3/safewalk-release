"""
    file:
        request.py
    purpose:
        Defines object model that represents the Request database table
"""

from app.models import db

from datetime import datetime

from marshmallow import Schema, fields, pre_load, validate, ValidationError

# Table for information pertaining to an individual request
class Request(db.Model):
    # SCHEMA
    ID = db.Column(db.Integer, primary_key=True)
    timeStamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    fromLocation = db.Column(db.String(128), index=True)
    toLocation = db.Column(db.String(128), index=True)
    # One REQUEST links to many RESPONSES
    responses = db.relationship('Response', backref='request', lazy='dynamic') 
    
    # Save database changes
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    # Delete database elements
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    # Get element from table by ID
    @staticmethod
    def get(id) :
        return Request.query.get(id)

    # Get all elements
    @staticmethod
    def get_all():
        return Request.query.all()

    # String representation
    def __repr__(self):
        return '<Request {} from {} to {} at {}>'.format(self.ID, self.fromLocation, self.toLocation, self.toLocation)

# Schema to validate data that represents a Request element
class RequestSchema(Schema):
    ID = fields.Int(dump_only=True)
    timeStamp = fields.DateTime(required=True)
    fromLocation = fields.String(required=True)
    toLocation = fields.String(required=True)