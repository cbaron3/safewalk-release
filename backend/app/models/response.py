"""
    file:
        rating.py
    purpose:
        Defines object model that represents the Response database table
"""

from app.models import db

from datetime import datetime

from marshmallow import Schema, fields, pre_load, validate, ValidationError

# Table for information pertaining to an individual response
class Response(db.Model):
    # SCHEMA
    ID = db.Column(db.Integer, primary_key=True)
    requestID = db.Column(db.Integer, db.ForeignKey('request.ID'))
    overallRating = db.Column(db.Float)
    pathPolyline = db.Column(db.String(128))
    # One RESPONSE links to many RATINGS
    ratings = db.relationship('Rating', backref='rating', lazy='dynamic') 

    # Save database database changes
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
        return Response.query.get(id)

    # Get all elements
    @staticmethod
    def get_all():
        return Response.query.all()

    # String representation
    def __repr__(self):
        return '<Response {} from Request {} with rating {} and polyline {}>'.format(self.ID, self.requestID, self.overallRating, self.pathPolyline)

# Schema to validate data that represents a Response element
class ResponseSchema(Schema):
    ID = fields.Int(dump_only=True)
    requestID = fields.Int(dump_only=True)
    overallRating = fields.Float(requred=True)
    pathPolyline = fields.String(required=True)