from kasa import Discover, Module
import asyncio
import time
from typing import Callable, Any

class DeviceManager():

    def simulate_function(func: Callable[..., Any]) -> Callable[..., Any]:     # type: ignore[misc]
        def wrapper(self, *args, **kwargs):
            if self.simulate:
                print(f"Simulating: {func.__name__} with args: {args}, kwargs: {kwargs}")
                time.sleep(0.1)
                return None
            else:
                print(f"Calling: {func.__name__} with args: {args}, kwargs: {kwargs}")
                return func(self, *args, **kwargs)
        return wrapper
    
    def __init__(self, simulate=False):
        self.simulate = simulate
        self.devices = {}
        self.loop = asyncio.get_event_loop()
        devices = self.loop.run_until_complete(Discover.discover())
        for dev in devices.values():
            self.loop.run_until_complete(dev.update())
            if dev.alias is not None:
                self.devices[dev.alias] = dev

    @simulate_function
    def delay(self, milliseconds):
        print(f"""Delaying for {milliseconds} milliseconds""")
        self.loop.run_until_complete(asyncio.sleep(milliseconds / 1000))

    @simulate_function
    def change_light_color(self, light_name, h, s, v):
        print(f"""Changing "{light_name}" to {h}, {s}, {v}""")
        if light_name in self.devices:
            self.loop.run_until_complete(self.devices[light_name].modules[Module.Light].set_hsv(h, s, v))

    @simulate_function
    def turn_light_on_off(self, light_name, on):
        print(f"""Turning "{light_name}" on/off: {on}""")
        if light_name in self.devices:
            self.loop.run_until_complete(self.devices[light_name].turn_on() if on else self.devices[light_name].turn_off())
        else:
            print(f"""Light "{light_name}" not found""")
