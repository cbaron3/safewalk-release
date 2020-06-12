"""
    file: email.py
    purpose: Endpoint for handling contact emailing
"""

from flask import request as req

from flask_restful import Resource

from app.endpoints.util import HTTPHandler

from app import mail
from flask_mail import Message

from app.models.contact import ContactSchema

from marshmallow import ValidationError

contactSchema = ContactSchema()

def create_account_message(name, email, subject, message):
    """
        purpose: 
            Format text for email content thats sent to safewalks account
        parameters:
            name [str] - Name of sender 
            email [str] - Email of sender
            subject [str] - Subject of message
            message [str] - Message text
    """

    original = 'RECEIVED MESSAGE\n\
                \rFROM: {}, {}\n\
                \rSUBJECT: {}\n\
                \rMESSAGE: {}'.format(name, email, subject, message)

    return original

def create_user_message(name, email, subject, message):
    """
        purpose: 
            Format text for email content thats sent to a user confirming their message
        parameters:
            name [str] - Name of sender 
            email [str] - Email of sender
            subject [str] - Subject of message
            message [str] - Message text
    """
    start = 'Hello {},\n\n'.format(name)

    body = 'Thank you for contacting SafeWalks London! All feedback is appreciated.\n\
            \rIf your message contained an inquiry, we will try and respond as soon as possible.\n\n'
        
    end = 'Have a great day!\n\n\n'

    if not subject:
        subject = 'N/A'

    original = '\n\rORIGINAL MESSAGE\n\
                \rFROM: {}, {}\n\
                \rSUBJECT: {}\n\
                \rMESSAGE: {}'.format(name, email, subject, message)

    return start + body + end + original

class EmailResource(Resource):
    def post(self):
        """
            purpose:
                Send email to inbox for contact purposes
                Send email to user thanking them for their feedback
            parameters:
                Name
                Email
                Subject
                Message
            return:
                HTTP 400 - Error occured
                HTTP 200 - Successful
        """

        # Get JSON data
        json_data = req.get_json(force=False)
        print(json_data)
        if not json_data:
            return HTTPHandler.no_data()

        # Load contact data if possible
        try:
            data = contactSchema.load(json_data)
        except ValidationError as e:
            return HTTPHandler.improper_data(e)

        contact_failed = False

        # Send message confirming contact
        try:
            mail.send_message(
                subject='SafeWalk - Message Received',
                sender='safewalklondonon@gmail.com',
                recipients=[data['email']],
                body = create_user_message(data['name'], data['email'], data['subject'], data['message']))
        except Exception as e:
            contact_failed = True
            print(e)
        
        # If contact to user did not fail, forward message to safewalks account
        if not contact_failed:
            try:
                mail.send_message(
                    subject='SafeWalk - New Message',
                    sender='safewalklondonon@gmail.com',
                    recipients=['safewalklondonon@gmail.com'],
                    body = create_account_message(data['name'], data['email'], data['subject'], data['message']))
            except Exception as e:
                print(e)

        #safewalklondonon@gmail.com
        #walksafe1119!

        return HTTPHandler.valid()