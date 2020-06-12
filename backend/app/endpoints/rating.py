"""
    file: rating.py
    purpose: Endpoints for accessing/modifying ratings via Request and Response IDs
"""

from flask import request as req
from flask_restful import Resource

from marshmallow import ValidationError
from app.models import db

from app.models.request import Request, RequestSchema
from app.models.rating import Rating, RatingSchema
from app.models.response import Response, ResponseSchema

from app.endpoints.util import HTTPHandler

ratingsSchema = RatingSchema(many=True)
ratingSchema = RatingSchema()

class RatingListResource(Resource):
    """
        Handle a list of ratings. Get all, update all, delete all, add
    """

    def get(self, request_id, response_id):
        """
            purpose: 
                Get all ratings for a response
            parameters:
                response_id - ID of response to get ratings from
                request_id - ID of request that is parent to the response
            return:
                HTTP 400 - Error occured
                HTTP 422 - Invalid ids
                HTTP 201 - List of ratings; JSON
        """

        try:
            # Get request by ID
            request = Request.query.get(request_id)
            if not request:
                return HTTPHandler.improper_id('Request')

            # Get response by ID
            response = Response.query.with_parent(request).filter(Response.ID == response_id).one()
            if not response:
                return HTTPHandler.improper_id('Response')

            # Get all ratings
            ratings = Rating.query.with_parent(response)
            ratings = ratingsSchema.dump(ratings)

            return HTTPHandler.valid_data(ratings)

        except Exception as e:
            return HTTPHandler.error(e)
    
    def put(self, request_id, response_id):
        """
            purpose:
                Update all ratings for a given response
            parameters:
                response_id - ID of response to update ratings for
                request_id - ID of request that is parent to the response
                json - json containing updated Rating data
                    {
                        'metricValue': ...
                        'metricType': ...
                    }
            return:
                HTTP 400 - Error occured
                HTTP 422 - Invalid ids or data
                HTTP 201 - List of updated ratings; JSON
        """

        # Get json data
        json_data = req.get_json(force=False)
        if not json_data:
            return HTTPHandler.no_data()

        # Load rating data if possible
        try:
            data = ratingSchema.load(json_data)
        except ValidationError as e:
            return HTTPHandler.improper_data(e)

        try:
            # Get request by ID
            request = Request.query.get(request_id)
            if not request:
                return HTTPHandler.improper_id('Request')

            # Get response by ID
            response = Response.query.with_parent(request).filter(Response.ID == response_id).one()
            if not response:
                return HTTPHandler.improper_id('Response')
            
            # Update rating element
            for r in response.ratings:
                r.metricType = data['metricType']
                r.metricValue = data['metricValue']

            # Save updates
            db.session.commit()
            
            return HTTPHandler.valid_data(ratingsSchema.dump(response.ratings))

        except Exception as e:
            return HTTPHandler.error(e)

    def post(self, request_id, response_id):
        """
            purpose:
                Add new rating to a given response
            parameters:
                response_id - ID of response to add rating too
                request_id - ID of request that is parent to the response
                json - json containing Rating data
                    {
                        'metricValue': ...
                        'metricType': ...
                    }
            return:
                HTTP 400 - Error occured
                HTTP 422 - Invalid ids or data
                HTTP 201 - Newly added rating; JSON
        """

        # Get json data
        json_data = req.get_json(force=False)
        if not json_data:
            return HTTPHandler.no_data()

        # Load rating data if possible
        try:
            data = ratingSchema.load(json_data)
        except ValidationError as e:
            return HTTPHandler.improper_data(e)

        try:
            # Get request by ID
            request = Request.query.get(request_id)
            if not request:
                return HTTPHandler.improper_id('Request')

            # Get response by ID
            response = Response.query.with_parent(request).filter(Response.ID == response_id).one()
            if not response:
                return HTTPHandler.improper_id('Response')

            # Creating rating element
            ratingElement = Rating(
                responseID = response_id,
                metricType = data['metricType'],
                metricValue = data['metricValue']
            )

            # Add rating element to response
            response.ratings.append(ratingElement)

            # Save to database
            ratingElement.save()

            return HTTPHandler.valid_data(ratingSchema.dump(ratingElement))

        except Exception as e:
            return HTTPHandler.error(e)

    def delete(self, request_id, response_id):
        """
            purpose:
                Delete all ratings for a given response
            parameters:
                response_id - ID of response to delete ratings from
                request_id - ID of request that is parent to the response
            return:
                HTTP 400 - Error occured
                HTTP 422 - Invalid ids
                HTTP 201 - Deleted ratings; JSON
        """

        try:
            # Get request by ID
            request = Request.query.get(request_id)
            if not request:
                return HTTPHandler.improper_id('Request')

            # Get response by ID
            response = Response.query.with_parent(request).filter(Response.ID == response_id).one()
            if not response:
                return HTTPHandler.improper_id('Response')

            ratings = ratingsSchema.dump(response.ratings)

            # Delete all ratings with response as parent
            Rating.query.with_parent(response).delete()

            # Update db
            db.session.commit()

            return HTTPHandler.valid_data(ratings)

        except Exception as e:
            return HTTPHandler.error(e)

class RatingResource(Resource):
    """
        Handle a single ratings. Get, update, delete
    """

    def get(self, request_id, response_id, rating_id):
        """
            purpose: 
                Get an individual rating
            parameters:
                rating_id - ID of rating
                response_id - ID of response that is parent to the rating
                request_id - ID of request that is parent to the response
            return:
                HTTP 400 - Error occured
                HTTP 422 - Invalid ids
                HTTP 201 - Rating; JSON
        """

        try:
            # Get request by ID
            request = Request.query.get(request_id)
            if not request:
                return HTTPHandler.improper_id('Request')

            # Get response by ID
            response = Response.query.with_parent(request).filter(Response.ID == response_id).one()
            if not response:
                return HTTPHandler.improper_id('Response')

            # Get rating by ID
            rating = Rating.query.with_parent(response).filter(Rating.ID == rating_id).one()
            if not rating:
                return HTTPHandler.improper_id('Rating')

            return HTTPHandler.valid_data(ratingSchema.dump(rating))

        except Exception as e:
            return HTTPHandler.error(e)
    
    def put(self, request_id, response_id, rating_id):
        """
            purpose:
                Update an individual rating
            parameters:
                rating_id - ID of rating
                response_id - ID of response that is parent to the rating
                request_id - ID of request that is parent to the response   
                json - json containing Rating data
                    {
                        'metricValue': ...
                        'metricType': ...
                    }
            return:
                HTTP 400 - Error occured
                HTTP 422 - Invalid ids or data
                HTTP 201 - Updated rating; JSON
        """

        # Get json data
        json_data = req.get_json(force=False)
        if not json_data:
            return HTTPHandler.no_data()

        # Load rating data if possible
        try:
            data = ratingSchema.load(json_data)
        except ValidationError as e:
            return HTTPHandler.improper_data(e)

        try:
            # Get request by ID
            request = Request.query.get(request_id)
            if not request:
                return HTTPHandler.improper_id('Request')

            # Get response by ID
            response = Response.query.with_parent(request).filter(Response.ID == response_id).one()
            if not response:
                return HTTPHandler.improper_id('Response')

            # Get rating by ID
            rating = Rating.query.with_parent(response).filter(Rating.ID == rating_id).one()
            if not rating:
                return HTTPHandler.improper_id('Rating')

            # Update element and save
            rating.metricType = data['metricType']
            rating.metricValue = data['metricValue']

            db.session.commit()

            return HTTPHandler.valid_data(ratingSchema.dump(rating))

        except Exception as e:
            return HTTPHandler.error(e)

    def delete(self, request_id, response_id, rating_id):
        """
            purpose:
                Delete an individual rating
            parameters:
                rating_id - ID of rating
                response_id - ID of response that is parent to the rating
                request_id - ID of request that is parent to the response   
            return:
                HTTP 400 - Error occured
                HTTP 422 - Invalid ids
                HTTP 201 - Deleted rating; JSON
        """
        
        try:
            # Get request by ID
            request = Request.query.get(request_id)
            if not request:
                return HTTPHandler.improper_id('Request')

            # Get response by ID
            response = Response.query.with_parent(request).filter(Response.ID == response_id).one()
            if not response:
                return HTTPHandler.improper_id('Response')

            # Get rating by ID
            rating = Rating.query.with_parent(response).filter(Rating.ID == rating_id).one()
            if not rating:
                return HTTPHandler.improper_id('Rating')

            # Store JSON before deleting instance
            rating_results = ratingSchema.dump(rating)

            # Delete
            rating.delete()

            return HTTPHandler.valid_data(rating_results)

        except Exception as e:
            return HTTPHandler.error(e)