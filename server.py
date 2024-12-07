from flask import Flask, request
from config import DEBUG, PORT, SIMULATE
from device_manager import DeviceManager
from chat_manager import ChatManager
from flask import request
from twilio.twiml.messaging_response import MessagingResponse
import threading
import time

def run(functions, stop_event):
    i = 0
    while i < len(functions) and not stop_event.is_set():
        function = functions[i]
        if function == "loop":
            i = 0
        else:
            function()
            i += 1
        time.sleep(0.1)

class Server():
    def __init__(self):
        self.device_manager = DeviceManager(simulate=SIMULATE)
        self.chat_manager = ChatManager(self.device_manager)
        self.app = Flask(__name__)
        self.app.add_url_rule("/sms", view_func=self.sms_reply, methods=['POST'])
        self.running_thread = None
        self.stop_event = threading.Event()

    def sms_reply(self):
        if self.running_thread and self.running_thread.is_alive():
            self.stop_event.set()
            self.running_thread.join(timeout=3)
            if self.running_thread.is_alive():
                print("Warning: Previous thread did not stop in time")

        user_input = request.values.get('Body', None)
        assistant_response = self.chat_manager.handle_message(user_input)
        self.stop_event.clear()
        self.running_thread = threading.Thread(target=run, args=(self.chat_manager.function_calls,self.stop_event))
        self.running_thread.start()

        resp = MessagingResponse()
        resp.message(assistant_response)
        return str(resp)

def main():
    Server().app.run(debug=DEBUG, port=PORT)

if __name__ == "__main__":
    main()
