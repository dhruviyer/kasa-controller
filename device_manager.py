from kasa import Discover, Module
import asyncio

class DeviceManager():

    def __init__(self, simulate=False):
        self.simulate = simulate
        self.devices = {}
        self.loop = asyncio.get_event_loop()
        devices = self.loop.run_until_complete(Discover.discover())
        for dev in devices.values():
            self.loop.run_until_complete(dev.update())
            if dev.alias is not None:
                self.devices[dev.alias] = dev

    def change_light_color(self, light_name, h, s, v):
        print(f"""Changing "{light_name}" to {h}, {s}, {v}""")
        if self.simulate:
            return
        if light_name in self.devices:
            self.loop.run_until_complete(self.devices[light_name].modules[Module.Light].set_hsv(h, s, v))

    def turn_light_on_off(self, light_name, on):
        print(f"""Turning "{light_name}" on/off: {on}""")
        if self.simulate:
            return
        if light_name in self.devices:
            self.loop.run_until_complete(self.devices[light_name].turn_on() if on else self.devices[light_name].turn_off())
        else:
            print(f"""Light "{light_name}" not found""")
