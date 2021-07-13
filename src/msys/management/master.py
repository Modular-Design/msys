from fastapi import FastAPI, Body
from .registration import Registration
from .factory import Factory

class Master(FastAPI):
    def __init__(self):
        self.registration = Registration()
        self.factory = Factory(self.registration)

        super().__init__(routes=[self.registration, self.factory])


