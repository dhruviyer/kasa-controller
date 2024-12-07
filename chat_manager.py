from openai import OpenAI
from function_definitions import get_light_color_control_function, get_turn_light_on_off_function, get_delay_function, get_loop_function
import json
from device_manager import DeviceManager
from config import MODEL
from functools import partial
import threading

class ChatManager():

    def __init__(self, device_manager: DeviceManager):
        self.client = OpenAI()
        self.messages = []
        self.device_manager = device_manager
        
        self.function_calls = []

        """Initialize the chat with system message"""

        self.messages.append({"role": "system", "content": """
            You are responsible for controlling the lights in the house.
            You can control the light colors using the set_light_color(light_name, hue, saturation, value) function.
            You can also turn lights on or off using the turn_light_on_off(light_name, on) function.
            You can set a delay using the delay(milliseconds) function.
            You can loop the previous commands using the loop() function.
        
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
                              
            VERY IMPORTANT: If you want to create a looped pattern, you must call loop. Do not simualte a loop by just repeating the same calls over and over again.
                              You can only call loop() one time. Before you call loop, you should add a small delay.

            NEVER tell a user that they have already sent a command, you don't know if your command was successful, so the user might ask you to retry
        """})

    def handle_message(self, user_input):
        """Handle user message and return assistant's response"""
        self.messages.append({"role": "user", "content": user_input})
        
        self.function_calls = []
        
        return_message = "Done!"

        for _ in range(100):  # Allow for multiple exchanges if needed
            # Get completion from OpenAI
            response = self.client.chat.completions.create(
                model=MODEL,
                messages=self.messages,
                tools=[get_light_color_control_function(self.device_manager.devices), get_turn_light_on_off_function(self.device_manager.devices), get_delay_function(), get_loop_function()]
            )
            
            # Handle any function calls from the model
            if response.choices[0].message.tool_calls:
                self.messages.append(response.choices[0].message)
                for tool_call in response.choices[0].message.tool_calls:
                    function_args = json.loads(tool_call.function.arguments)
                    print(f"Function call: {tool_call.function.name} with args: {function_args}")
                    if tool_call.function.name == "turn_light_on_off":
                        self.function_calls.append(partial(
                            self.device_manager.turn_light_on_off,
                            function_args["light_name"], 
                            function_args["on"]
                        ))
                        
                        self.messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": tool_call.function.name,
                            "content": "Light turned on/off successfully"
                        })
                        
                    elif tool_call.function.name == "set_light_color":
                        self.function_calls.append(partial(
                            self.device_manager.change_light_color,
                            function_args["light_name"],
                            function_args["hue"],
                            function_args["saturation"],
                            function_args["value"]
                        ))
                        
                        self.messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": tool_call.function.name,
                            "content": "Light color changed successfully"
                        })
                    elif tool_call.function.name == "delay":
                        # delay this thread for milliseconds
                        self.function_calls.append(partial(self.device_manager.delay, function_args["milliseconds"]))

                        self.messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": tool_call.function.name,
                            "content": "Delay completed successfully"
                        })
                    elif tool_call.function.name == "loop":
                        # delay this thread for milliseconds
                        self.function_calls.append("loop")

                        self.messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": tool_call.function.name,
                            "content": "Looped successfully"
                        })
            else:
                self.messages.append(response.choices[0].message)
                return_message = response.choices[0].message.content
                break      
        
        return return_message