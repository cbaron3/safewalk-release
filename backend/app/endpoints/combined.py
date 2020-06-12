"""
    file: combined.py
    purpose: Endpoints for accessing requests linked to responses and ratings
"""

from flask_restful import Resource

from app.endpoints.util import HTTPHandler

from app.models.request import Request, RequestSchema
from app.models.rating import Rating, RatingSchema
from app.models.response import Response, ResponseSchema

from app.models import db

requestsSchema = RequestSchema(many=True)
requestSchema  = RequestSchema()

ratingsSchema = RatingSchema(many=True)
ratingSchema = RatingSchema()

responsesSchema = ResponseSchema(many=True)
responseSchema = ResponseSchema()

class CombinedListResource(Resource):
    def get(self):
        """
            purpose: 
                Get all requests; including all responses and ratings
            parameters:
                None
            return:
                HTTP 400 - Error occured 
                HTTP 201 - Successful, json = {
                    'status': 'success',
                    'data' : [
                        {
                            request data ...
                            'responses': [
                                {
                                    response data...
                                    'ratings' = [
                                        {
                                            rating data...
                                        },
                                    ]
                                },
                            ]
                        },
                    ]
                }
        """
        
        try:
            # Get requests as database object and JSO
            requests_db = Request.query.all()
            requests = requestsSchema.dump(requests_db)

            # For each request, link response and rating JSON
            for i in range(len(requests)):
                
                # Get responses as database object and JSON
                responses_db = Response.query.with_parent(requests_db[i])
                responses = responsesSchema.dump(responses_db)

                # For each response, link rating JSON
                for j in range(len(responses)):
                    rating = Rating.query.with_parent(responses_db[j])
                    rating = ratingsSchema.dump(rating)
                    responses[j]['ratings'] = rating
                
                requests[i]['responses'] = responses

            return HTTPHandler.valid_data(requests)

        except Exception as e:
            return HTTPHandler.error(e)

class CombinedResource(Resource):
    def get(self, id):
        """
            purpose: 
                Get a requests by ID; including all responses and ratings
            parameters:
                id - request id
            return:
                HTTP 400 - Error occured
                HTTP 422 - Invalid id
                HTTP 201 - Successful, json = {
                    'status': 'success',
                    'data' :
                        request data ...
                        'responses': [
                            {
                                response data...
                                'ratings' = [
                                    {
                                        rating data...
                                    },
                                ]
                            },
                        ]
                }
        """

        try:
            # Get request as database object and JSON
            request_db = Request.query.get(id)
            if not request_db:
                return HTTPHandler.improper_id()

            request = requestSchema.dump(request_db)
                
            # Get responses for request as database object and JSON
            responses_db = Response.query.with_parent(request_db)
            responses = responsesSchema.dump(responses_db)

            # For each response, link rating JSON
            for i in range(len(responses)):
                rating = Rating.query.with_parent(responses_db[i])
                rating = ratingsSchema.dump(rating)
                responses[i]['ratings'] = rating
            
            request['responses'] = responses

            return HTTPHandler.valid_data(request)
        except Exception as e:
            return HTTPHandler.error(e)