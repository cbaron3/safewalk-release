from flask import Flask, Blueprint
from flask_restful import Api
from flask_cors import CORS

# Create API blueprint with /api as URL base
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Create mail connection
from flask_mail import Mail
mail = Mail()

# Google maps API access
import os
from app.metrics.map import GMapsAPI
gmaps = GMapsAPI(os.getenv('FLASK_APP_BACKEND_GMAPS_API_KEY'))

status = gmaps.create_conn()
if not status:
    print('Maps API failed to connect')

# Algorithm solver
from app.metrics.algorithm import RatingAlgorithms
algos = RatingAlgorithms()

# Open data threaded access
from app.metrics.opendata import DataThreadPool
datapool = DataThreadPool()

# Combined data
from app.endpoints.combined import CombinedResource, CombinedListResource
api.add_resource(CombinedResource, '/<id>')
api.add_resource(CombinedListResource, '/')

# Requests
from app.endpoints.request import RequestResource, RequestListResource
api.add_resource(RequestResource, '/request/<request_id>')
api.add_resource(RequestListResource, '/request')

# Responses
from app.endpoints.response import ResponseResource, ResponseListResource
api.add_resource(ResponseResource, '/request/<request_id>/response/<response_id>')
api.add_resource(ResponseListResource, '/request/<request_id>/response')

# Ratings
from app.endpoints.rating import RatingResource, RatingListResource
api.add_resource(RatingResource, '/request/<request_id>/response/<response_id>/rating/<rating_id>')
api.add_resource(RatingListResource, '/request/<request_id>/response/<response_id>/rating')

# Calculate Ratings
from app.endpoints.calculate_rating import CalcRatingResource
api.add_resource(CalcRatingResource, '/calc_rating')

# Email
from app.endpoints.email import EmailResource
api.add_resource(EmailResource, '/email')

def create_app(config_object):
    app = Flask(__name__)

    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000, safewalklondon.ca"}})

    app.config.from_object(config_object)
    
    mail.init_app(app)

    from app import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    from app.models import db
    db.init_app(app)

    return app