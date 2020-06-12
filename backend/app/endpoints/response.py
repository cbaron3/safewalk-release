"""
    file: response.py
    purpose: Endpoints for accessing/modifying responses via Request ID
"""

from flask import request as req
from flask_restful import Resource

from app.models import db

from app.models.request import Request, RequestSchema
from app.models.rating import Rating, RatingSchema
from app.models.response import Response, ResponseSchema

from app.endpoints.util import HTTPHandler

responsesSchema = ResponseSchema(many=True)

responseSchema = ResponseSchema()

class ResponseListResource(Resource):
    """
        Handle a list of responses. Get all, update all, delete all, add
    """

    def get(self, request_id):
        """
            purpose:
                Get all response resources pertaining to a specific request
            parameter:
                request_id - ID of request that is parent to the response  
            return:
                HTTP 400 - Error occured
                HTTP 422 - Invalid id
                HTTP 201 - List of responses; JSON
        """

        try:
            # Get request by ID
            request = Request.query.get(request_id)
            if not request:
                return HTTPHandler.improper_id('Request')

            # Return response data
            return HTTPHandler.valid_data( responsesSchema.dump(request.responses) )

        except Exception as e:
            return HTTPHandler.error(e)
    
    def put(self, request_id):
        """
            purpose:
                Update all response resources pertaining to a specific request
            parameter:
                request_id - ID of request that is parent to the response  
                json - json containing Response data:
                    {
                        "overallRating": ...
                        "pathPolyline": ...
                    }
            return:
                HTTP 400 - Error occured
                HTTP 422 - Invalid id or data
                HTTP 201 - List of updated responses; JSON
        """

        # Get json data
        json_data = req.get_json(force=False)
        if not json_data:
            return HTTPHandler.no_data()

        # Load response data if possible
        try:
            data = responseSchema.load(json_data)
        except Exception as e:
            return HTTPHandler.improper_data(e)

        try:
            # Get request by ID
            request = Request.query.get(request_id)
            if not request:
                return HTTPHandler.improper_id('Request')

            # Update each response linked to the parent request
            for r in request.responses:
                r.overallRating = data['overallRating']
                r.pathPolyline = data['pathPolyline']

            # Save changes
            db.session.commit()
            
            # Return response data
            return HTTPHandler.valid_data( responsesSchema.dump(request.responses))

        except Exception as e:
            return HTTPHandler.error(e)

    def post(self, request_id):
        """
            purpose:
                Create a new response linked to a specific request
            parameter:
                request_id - ID of request that is parent to the response  
                json - json containing Response data:
                    {
                        "overallRating": ...
                        "pathPolyline": ...
                    }
            return:
                HTTP 400 - Error occured
                HTTP 422 - Invalid id or data
                HTTP 201 - New response; JSON
        """

        # Get json data
        json_data = req.get_json(force=False)
        if not json_data:
            return HTTPHandler.no_data()

        # Load response data if possible
        try:
            data = responseSchema.load(json_data)
        except Exception as e:
            return HTTPHandler.improper_data(e)

        try:
            # Get request by ID
            request = Request.query.get(request_id)
            if not request:
                return HTTPHandler.improper_id('Request')
            
            # Create new response ID
            new_response = Response(
                requestID = request_id,
                overallRating = data['overallRating'],
                pathPolyline = data['pathPolyline']
            )

            # Link new response with parent request
            request.responses.append(new_response)
            new_response.save()

            # Return newly created response
            return HTTPHandler.valid_data( responseSchema.dump(new_response) )
        
        except Exception as e:
            return HTTPHandler.error(e)


    def delete(self, request_id):
        """
            purpose:
                Delete all responses linked to a specific request
            parameter:
                request_id - ID of request that is parent to the response  
            return:
                HTTP 400 - Error occured
                HTTP 422 - Invalid ids
                HTTP 201 - List of deleted responses; JSON
        """

        try:
            # Get request by ID
            request = Request.query.get(request_id)
            if not request:
                return HTTPHandler.improper_id('Request')

            # Dump response data pertaining to responses that will be deleted
            resps = responsesSchema.dump(request.responses)

            # Delete responses
            Response.query.with_parent(request).delete()
            db.session.commit()

            return HTTPHandler.valid_data( resps )

        except Exception as e:
            return HTTPHandler.error(e)

class ResponseResource(Resource):
    """
        Handle a single response. Get, update, delete
    """
    
    def get(self, request_id, response_id):
        """
            purpose:
                Get a response linked to a specific request
            parameter:
                response_id - ID of response
                request_id - ID of request that is parent to the response
            return:
                HTTP 400 - Error occured
                HTTP 422 - Invalid ids
                HTTP 201 - Response; JSON
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

            return HTTPHandler.valid_data( responseSchema.dump(response) )

        except Exception as e:
            return HTTPHandler.error(e)

    def put(self, request_id, response_id):
        """
            purpose:
                Update a response linked to a specific request
            parameter:
                response_id - ID of response
                request_id - ID of request that is parent to the response  
                json - json containing Response data:
                    {
                        "overallRating": ...
                        "pathPolyline": ...
                    }
            return:
                HTTP 400 - Error occured
                HTTP 422 - Invalid ids or data
                HTTP 201 - Response; JSON
        """

        # Get json data
        json_data = req.get_json(force=False)
        if not json_data:
            return HTTPHandler.no_data()

        # Load response data if possible
        try:
            data = responseSchema.load(json_data)
        except Exception as e:
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

            response.overallRating = data['overallRating']
            response.pathPolyline = data['pathPolyline']

            db.session.commit()

            return HTTPHandler.valid_data( responseSchema.dump(response) )

        except Exception as e:
            return HTTPHandler.error(e)

    def delete(self, request_id, response_id):
        """
            purpose: 
                Delete an individual response linked to a specific request
            parameters:
                response_id - ID of response
                request_id - ID of request that is parent to the response  
            return:
                HTTP 400 - Error occured
                HTTP 422 - Invalid id
                HTTP 201 - Deleted request; JSON
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

            # Store data before deleting
            resp_data = responseSchema.dump(response)
            
            response.delete()

            return HTTPHandler.valid_data( resp_data )

        except Exception as e:
            return HTTPHandler.error(e)