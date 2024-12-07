from kasa import Module
from openai.types.chat import ChatCompletionToolParam


def get_loop_function() -> ChatCompletionToolParam:
    return {
        "type": "function",
        "function": {
            "name": "loop",
            "description": "Loops the previous commands",
            "parameters": {},
            }
        }
    


def get_delay_function() -> ChatCompletionToolParam:
    return {
        "type": "function",
        "function": {
            "name": "delay",
            "description": "Delay for a number of milliseconds, use this when you need to implement transitions",
            "parameters": {
                "type": "object",
                "properties": {
                    "milliseconds": {
                        "type": "integer",
                        "description": "Number of milliseconds to delay"
                    }
                },
                "required": ["milliseconds"]
            }
        }
    }

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
                        "type": "integer",
                        "description": "Hue value between 0-360",
                        "minimum": 0,
                        "maximum": 360
                    },
                    "saturation": {
                        "type": "integer", 
                        "description": "Saturation percentage between 0-100",
                        "minimum": 0,
                        "maximum": 100
                    },
                    "value": {
                        "type": "integer",
                        "description": "Brightness value between 0-100",
                        "minimum": 0,
                        "maximum": 100
                    }
                },
                "required": ["hue", "saturation", "value"]
            }
        }
    }

def get_turn_light_on_off_function(device_configs) -> ChatCompletionToolParam:
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
