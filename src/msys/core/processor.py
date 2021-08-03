from .helpers import find_open_ports
import subprocess as sp
import requests
import json
from typing import Optional


class Processor:
    def __init__(self,
                 id,
                 location: Optional[str] = None,
                 remote: Optional[str] = "",
                 users: Optional[int]=0):
        self.id = id
        self.launch = location
        self.process = None
        self.url = remote
        self.port = -1
        self.users = users

        self.started = False
        self.start()

    def increase_users(self):
        self.users = self.users +1

    def decrease_users(self):
        if self.users > 0:
            self.users = self.users -1

    def start(self):
        self.increase_users()

        if self.users > 1 or self.started:
            return

        if self.launch:
            if type(self.launch) == str:
                if self.launch.find("{port}") != -1:
                    self.port = find_open_ports()
                    self.url = "http://127.0.0.1:{port}".replace("{port}", str(self.port))
                    cmd = self.launch.replace("{port}", str(self.port))
                    self.process = sp.Popen(cmd)

        self.started = True

    def stop(self):
        self.decrease_users()

        if self.users > 0 or not self.started:
            return

        self.kill()

    def kill(self):
        print("[Process] will be killed: " + self.url)
        if self.launch:
            ptype = type(self.process)
            if ptype == sp.Popen:
                self.process.terminate()
            else:
                print("[Process] dont found: " + str(ptype))

        self.started = False

    def get_config(self) -> dict:
        if self.url:
            response = requests.get(self.url + "/config")
            if response.status_code != 200:
                return dict()
            return json.loads(response.content)
        print("[Processor] no url")

    def change_config(self, config:dict) -> dict:
        if self.url:
            response = requests.post(self.url + "/config", config)
            if response.status_code != 200:
                return dict()
            return json.loads(response.content)
        print("[Processor] no url")

    def update_config(self, config:dict) -> dict:
        if self.url:
            response = requests.put(self.url + "/update", config)
            if response.status_code != 200:
                return dict()
            return json.loads(response.content)
        print("[Processor] no url")

    def __del__(self):
        self.kill()