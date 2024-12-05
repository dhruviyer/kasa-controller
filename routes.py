from flask import request
from twilio.twiml.messaging_response import MessagingResponse
from chat_manager import ChatManager

def register_routes(app, chat_manager: ChatManager):
    @app.route("/sms", methods=['GET', 'POST'])
    def sms_reply():
        user_input = request.values.get('Body', None)
        assistant_response = chat_manager.handle_message(user_input)
        resp = MessagingResponse()
        resp.message(assistant_response)
        return str(resp)