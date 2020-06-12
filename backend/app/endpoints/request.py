"""
    file: request.py
    purpose: Endpoints for accessing/modifying requests
"""

from flask import request as req
from flask_restful import Resource

from app.models import db

from app.models.request import Request, RequestSchema
from app.models.rating import Rating, RatingSchema
from app.models.response import Response, ResponseSchema

from app.endpoints.util import HTTPHandler

# Create schema wrapper that handles a list of requests
requestsSchema = RequestSchema(many=True)

# Create schema wrapper that handles a single request
requestSchema  = RequestSchema()

class RequestListResource(Resource):
    """
        Handle a list of requests. Get all, update all, delete all, add
    """

    def get(self):
        """
            purpose: 
                Get all request resources
            return:
                HTTP 400 - Error occured
                HTTP 201 - List of requests; JSON
        """

        try:
            requests = Request.get_all()
            return HTTPHandler.valid_data( requestsSchema.dump(requests) )
            
        except Exception as e:
            return HTTPHandler.error(e)
        
    def put(self):
        """
            purpose: 
                Updates all request resources
            parameters:
                json - json containing updated Response data
                    {
                        "timeStamp" : ...
                        "fromLocation": ...
                        "toLocation": ...
                    }
            return:
                HTTP 400 - Error occured
                HTTP 422 - Invalid data
                HTTP 201 - List of updated requests; JSON
        """

        # Get json data
        json_data = req.get_json(force=False)
        if not json_data:
            return HTTPHandler.no_data()

        # Load request data if possible
        try:
            data = requestSchema.load(json_data)
        except Exception as e:
            return HTTPHandler.improper_data(e)

        try:
            # Get all requests
            requests = Request.get_all()

            # Update each request
            for r in requests:
                r.timeStamp = data['timeStamp']
                r.fromLocation = data['fromLocation']
                r.toLocation = data['toLocation']

            # Save changes
            db.session.commit()

            return HTTPHandler.valid_data( requestsSchema.dump(requests) )

        except Exception as e:
            return HTTPHandler.error(e)

    def post(self):
        """
            purpose: 
                Create a new request 
            parameters:
                json - json containing Request data
                    {
                        "timeStamp" : ...
                        "fromLocation": ...
                        "toLocation": ...
                    }
            return:
                HTTP 400 - Error occured
                HTTP 422 - Invalid data
                HTTP 201 - New request; JSON
        """

        # Get json data
        json_data = req.get_json(force=False)
        if not json_data:
            return HTTPHandler.no_data()

        # Load request data if possible
        try:
            data = requestSchema.load(json_data)
        except Exception as e:
            return HTTPHandler.improper_data(e)

        try:
            # Create new request
            new_request = Request(
                timeStamp = data['timeStamp'],
                fromLocation = data['fromLocation'],
                toLocation = data['toLocation']
            )

            # Save the new request into the DB
            new_request.save()

            return HTTPHandler.valid_data( requestSchema.dump(new_request) )

        except Exception as e:
            return HTTPHandler.error(e)

    def delete(self):
        """
            purpose: 
                Delete all requests
            return:
                HTTP 400 - Error occured
                HTTP 201 - Deleted requests; JSON
        """

        try:
            # Returns the requests that will be deleted
            requests = Request.get_all()
            requests = requestsSchema.dump(requests)

            # Delete and save new DB status
            Request.query.delete()
            db.session.commit()

            return HTTPHandler.valid_data(requests)

        except Exception as e:
            return HTTPHandler.error(e)

class RequestResource(Resource):
    """
        Handle a single request. Get, update, delete
    """

    def get(self, request_id):
        """
            purpose: 
                Get an individual request
            parameters:
                request_id - ID of request
            return:
                HTTP 400 - Error occured
                HTTP 422 - Invalid id
                HTTP 201 - Request; JSON
        """

        try:
            # Get request by ID
            request = Request.query.get(request_id)
            if not request:
                return HTTPHandler.improper_id('Request')

            # Return data if exists
            return HTTPHandler.valid_data( requestSchema.dump(request) )

        except Exception as e:
            return HTTPHandler.error(e)
     
    
    def put(self, request_id):
        """
            purpose: 
                Update an individual request
            parameters:
                request_id - ID of request
                json - json containing Request data
                    {
                        "timeStamp" : ...
                        "fromLocation": ...
                        "toLocation": ...
                    }
            return:
                HTTP 400 - Error occured
                HTTP 422 - Invalid id or data
                HTTP 201 - Updated resquest; JSON
        """

        # Get json data
        json_data = req.get_json(force=False)
        if not json_data:
            return HTTPHandler.no_data()

        # Load request data if possible
        try:
            data = requestSchema.load(json_data)
        except Exception as e:
            return HTTPHandler.improper_data(e)

        try:
            # Get request by ID
            request = Request.query.get(request_id)
            if not request:
                return HTTPHandler.improper_id('Request')
        
            # If request exists, update data.
            request.timeStamp = data['timeStamp']
            request.fromLocation = data['fromLocation']
            request.toLocation = data['toLocation']

            db.session.commit()

            return HTTPHandler.valid_data( requestSchema.dump(request) )

        except Exception as e:
            return HTTPHandler.error(e)

    def delete(self, request_id):
        """
            purpose: 
                Delete an individual request
            parameters:
                request_id - ID of request
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

            # Dump before deleting so reference still exists
            request_result = requestSchema.dump(request)

            request.delete()

            return HTTPHandler.valid_data(request_result)

        except Exception as e:
            return HTTPHandler.error(e)