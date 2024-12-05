from kasa import Module
from openai.types.chat import ChatCompletionToolParam

def get_light_color_control_function(device_configs) -> ChatCompletionToolParam:
    return {
        "type": "function",
        "function": {
            "name": "set_light_color",
            "description": """Set the HSV color values for a light""",
            "parameters": {
                "type": "object",
                "properties": {
                    "light_name": {
                        "type": "string",
                        "description": "Name of the light to control",
                        "enum": list(filter(lambda x: Module.Light in device_configs[x].modules, device_configs.keys()))
                    },
                    "hue": {
                        "type": "number",
                        "description": "Hue value between 0-360",
                        "minimum": 0,
                        "maximum": 360
                    },
                    "saturation": {
                        "type": "number", 
                        "description": "Saturation percentage between 0-100",
                        "minimum": 0,
                        "maximum": 100
                    },
                    "value": {
                        "type": "number",
                        "description": "Brightness value between 0-100",
                        "minimum": 0,
                        "maximum": 100
                    }
                },
                "required": ["hue", "saturation", "value"]
            }
        }
    }

def turn_light_on_off_function(device_configs) -> ChatCompletionToolParam:
    return {
        "type": "function",
        "function": {
            "name": "turn_light_on_off",
            "description": "Turn a light on or off",
            "parameters": {
                "type": "object",
                "properties": {
                    "light_name": {
                        "type": "string",
                        "description": "Name of the light to control",
                        "enum": list(device_configs.keys())
                    },
                    "on": {
                        "type": "boolean",
                        "description": "True to turn the light on, False to turn it off"
                    }
                },
                "required": ["light_name", "on"]
            }
        }
    }
