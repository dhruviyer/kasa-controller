from flask import Flask
from config import DEBUG, PORT, SIMULATE
from device_manager import DeviceManager
from chat_manager import ChatManager
from routes import register_routes

app = Flask(__name__)

def main():
    device_manager = DeviceManager(simulate=SIMULATE)
    chat_manager = ChatManager(device_manager)
    register_routes(app, chat_manager)
    app.run(debug=DEBUG, port=PORT)

if __name__ == "__main__":
    main()
