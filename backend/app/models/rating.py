"""
    file:
        rating.py
    purpose:
        Defines object model that represents the Rating database table
"""

from app.models import db

from datetime import datetime

from marshmallow import Schema, fields, pre_load, validate, ValidationError

# Table for information pertaining to an individual rating
class Rating(db.Model):
    # SCHEMA
    ID = db.Column(db.Integer, primary_key=True)
    metricType = db.Column(db.String(128))
    metricValue = db.Column(db.Float)
    responseID = db.Column(db.Integer, db.ForeignKey('response.ID'))

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
        return Rating.query.get(id)

    # Get all elements
    @staticmethod
    def get_all():
        return Rating.query.all()

    # String representation
    def __repr__(self):
        return '<Rating {} from Response {} with type {} and value {}>'.format(self.ID, self.responseID, self.metricType, self.metricValue)

# Schema to validate data that represents a Rating element
class RatingSchema(Schema):
    ID = fields.Int(dump_only=True)
    responseID = fields.Int(dump_only=True)
    metricValue = fields.Float(required=True)
    metricType = fields.String(required=True)