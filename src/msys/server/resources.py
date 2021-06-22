import psutil
from fastapi import APIRouter, Body


class Resources(APIRouter):
    def __init__(self):
        super().__init__(prefix="/resources", tags=["resources"])
        self.cpu = 0
        self.ram = dict()

        @self.get("")
        async def all_resources():
            """lists alls extensions"""
            self.update_cpu()
            self.update_ram()
            return dict(cpu=self.cpu, ram=self.ram)

        @self.get("/cpu")
        async def cpu():
            """lists alls extensions"""
            self.update_cpu()
            return self.cpu

        @self.get("/ram")
        async def ram():
            """lists alls extensions"""
            self.get_ram()
            return self.ram

    def update_cpu(self):
        self.cpu=psutil.cpu_percent(4)

    def update_ram(self):
        ram = psutil.virtual_memory()
        self.ram = dict(total=ram[0], available=ram[1], used=ram[3], free=ram[4])