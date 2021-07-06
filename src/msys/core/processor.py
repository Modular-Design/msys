from .helpers import find_open_ports
import uvicorn
import multiprocessing as mp
import subprocess as sp
import inspect

class Processor():
    def __init__(self, launch):
        self.launch = launch
        self.process = None
        self.url = "http://127.0.0.1:{port}"
        self.port = -1

    def get_uri(self):
        return self.url

    def start(self):
        self.url = "http://127.0.0.1:{port}"
        self.port = find_open_ports()
        self.url = self.url.replace("{port}", str(self.port))
        if type(self.launch) == str:
            cmd = self.launch.replace("{port}", str(self.port))
            self.process = sp.Popen(cmd)

        return self.url

    def stop(self):
        ptype = type(self.process)
        if ptype == sp.Popen:
            self.process.terminate()
        elif ptype == mp.Process:
            self.process.join()
            self.process.kill()
        else:
            print("[Process] dont found: " + str(ptype))
