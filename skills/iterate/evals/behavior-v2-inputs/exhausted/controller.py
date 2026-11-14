"""Cancellation controller for a small request client."""
class Controller:
    def __init__(self, transport):
        self.transport = transport
        self.active = False

    def begin(self):
        self.active = True

    def complete(self):
        self.active = False

    def stop(self):
        if self.active:
            self.active = False
