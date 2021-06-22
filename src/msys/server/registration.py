from fastapi import APIRouter, Body

class Registration(APIRouter):
    def __init__(self):
        super().__init__(prefix="/registration", tags=["registration"])
        self.registered = dict()

        @self.get("")
        async def lists():
            """lists alls modules"""

        @self.post("")
        async def register(
                body=Body(
                    ...,
                    examples={
                        "child": {
                            "summary": "register with seperate startup",
                            "description": "A **child** service will be created and terminated by the server.",
                            "value": {
                                "startup": "C:/process.exe --host {host} --port {port} --uri {host}:{post}",
                                "name": "Child",
                            },
                        },
                        "independent": {
                            "summary": "register as an independent service",
                            "description": "A **independent** service will not be created or terminated by the server.",
                            "value": {
                                "connect": "127.0.0.1:8080",
                                "name": "Independent",
                            },
                        },
                        "parallel": {
                            "summary": "register as an parallel runnable service",
                            "description": "A **parallel** service will be created and terminated by the server and can have multiple instances.",
                            "value": {
                                "parallel": "C:/process.exe --host {host} --port {port} --uri {host}:{post}",
                                "name": "Parallel",
                            },
                        },
                    }
                )
        ):
            """lists alls modules"""
            pass

        @self.delete("")
        async def delete(
                body=Body(
                    ...,
                    examples={
                        "child": {
                            "summary": "delete with seperate startup",
                            "description": "A **child** service will be created and terminated by the server.",
                            "value": {
                                "startup": "C:/process.exe --host {host} --port {port} --uri {host}:{post}",
                            },
                        },
                        "independent": {
                            "summary": "delete as an independent service",
                            "description": "A **independent** service will not be created or terminated by the server.",
                            "value": {
                                "connect": "127.0.0.1:8080",
                            },
                        },
                    }
                )
        ):
            """lists alls modules"""
            pass