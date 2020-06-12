"""
    file: util.py
    purpose: Encapsulate utility functions for the endpoint module
"""

class HTTPHandler:
    """
        purpose: Single point of entry for handling http messages
    """

    @staticmethod
    def valid_data(msg):
        # Valid data is returned; 201 code
        return { 'status': 'success', 'data': msg }, 201

    @staticmethod
    def valid():
        # Valid data is returned; 201 code
        return { 'status': 'success' }, 200

    @staticmethod
    def error(msg):
        # Error is handled and returned; 400 code
        return {'status': 'failure', 'message': str(msg)}, 400

    @staticmethod
    def no_data():
        # No data is handled and returned; 400 code
        return {'status': 'failure', 'message': 'No input data provided'}, 400

    @staticmethod
    def improper_data(msg):
        # Improper data is handled and returned; 422 code
        return {'status': 'failure', 'message': 'Invalid data', 'error': str(msg)}, 422

    @staticmethod
    def improper_id(msg=None):
        # Improper id is handled and returned; 422 code

        # Gives the user the option to specify the type of ID
        if not msg:
            msg = ''

        return {'status': 'failure', 'message': 'Invalid {} ID'.format(msg)}, 422
