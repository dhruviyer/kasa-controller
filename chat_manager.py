from openai import OpenAI
from function_definitions import get_light_color_control_function, turn_light_on_off_function
import json
from device_manager import DeviceManager
from config import MODEL

class ChatManager():

    def __init__(self, device_manager: DeviceManager):
        self.client = OpenAI()
        self.messages = []
        self.device_manager = device_manager

        """Initialize the chat with system message"""

        self.messages.append({"role": "system", "content": """
            You are responsible for controlling the lights in the house.
            You can control the light colors using the set_light_color(light_name, hue, saturation, value) function.
            You can also turn lights on or off using the turn_light_on_off(light_name, on) function.
                        
            The lights are located either in the living room or the bedroom.
                       
            These lights are in the living room (the couch is directly opposite the TV). If the user generally refers to the lights in the living room, you should control these lights.

            It is very important to note that even though "couch left" and "couch right" do not have living room in the name, they still are considered to be part of the living room.             
            - Living room left: In the living room, left to the user, adjacent to the TV
            - Living room right: In the living room, right to the user, adjacent to the TV
            - Couch left: In the living room, left to the user, adjacent to the couch
            - Couch right: In the living room, right to the user, adjacent to the couch
                                
            These lights are in the bedroom. If the user generally refers to the lights in the bedroom, you should control these lights.
            - Bed left
            - Bed right
        """})

    def handle_message(self, user_input):
        """Handle user message and return assistant's response"""
        self.messages.append({"role": "user", "content": user_input})
        
        for _ in range(10):  # Allow for multiple exchanges if needed
            # Get completion from OpenAI
            response = self.client.chat.completions.create(
                model=MODEL,
                messages=self.messages,
                tools=[get_light_color_control_function(self.device_manager.devices), turn_light_on_off_function(self.device_manager.devices)]
            )
            
            # Handle any function calls from the model
            if response.choices[0].message.tool_calls:
                self.messages.append(response.choices[0].message)
                for tool_call in response.choices[0].message.tool_calls:
                    function_args = json.loads(tool_call.function.arguments)
                    
                    if tool_call.function.name == "turn_light_on_off":
                        self.device_manager.turn_light_on_off(
                            function_args["light_name"], 
                            function_args["on"]
                        )
                        
                        self.messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": tool_call.function.name,
                            "content": "Light turned on/off successfully"
                        })
                        
                    elif tool_call.function.name == "set_light_color":
                        self.device_manager.change_light_color(
                            function_args["light_name"],
                            function_args["hue"],
                            function_args["saturation"],
                            function_args["value"]
                        )
                        
                        self.messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": tool_call.function.name,
                            "content": "Light color changed successfully"
                        })
            else:
                assistant_response = response.choices[0].message.content
                self.messages.append({"role": "assistant", "content": assistant_response})
                return assistant_response