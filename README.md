# Kasa Controller

This project is a web-enabled AI assistant to control TP-Link Kasa smart home devices. It allows you to text (or ping a web endpoint) to control your smart home devices via natural language.

The project utilizes the `python-kasa` library to interact with Kasa devices and provides a simple interface for managing your smart home setup.

## Setting Up the Project

### Prerequisites

- Python 3.8 or newer
- pip (Python package installer)

### Creating a Virtual Environment and Installing Dependencies

1. Clone this repository:

   ```
   git clone https://github.com/dhruviyer/kasa-controller.git
   cd kasa-controller
   ```

2. Create a virtual environment:

   ```
   python -m venv venv
   ```

3. Activate the virtual environment:

   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```
   - On Windows:
     ```
     venv\Scripts\activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

This will install all necessary dependencies, including `python-kasa`, `openai`, and other required libraries.

## Customize the system message

If you look at `chat_manager.py`, you will see the following system message:

```
You are responsible for controlling the lights in the house.
You can control the light colors using the set_light_color(light_name, hue, saturation, value) function.
You can also turn lights on or off using the turn_light_on_off(light_name, on) function.

The lights are located either in the living room or the bedroom.

These lights are in the living room (the couch is directly opposite the TV). If the user generally refers to the lights in the living room, you should control these lights.

...
```

You will want to customize this message to fit your use case, which includes your own description of the lights in the house and where they are located.

## Usage

Start the server by running this command

```
python server.py
```

You can then make a POST request to `http://localhost:5000/sms` with the following JSON body:

```
{
    "Body": "Turn on the living room light"
}
```

## Twilio

In order to enable SMS texting for the app, you will need to expose the server using ngrok. Then you'll want to set up a Twilio phone number and webhook to call this API. For more information, see [this guide](https://www.twilio.com/docs/messaging/tutorials/how-to-receive-and-reply/python)
