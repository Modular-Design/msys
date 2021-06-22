import click
import uvicorn
from ..server.server import MSYSServer
from ..registration import *

server = MSYSServer()

def launch(module="msys.scripts.msys:server", host= "127.0.0.1", port=9000):
    uvicorn.run(module, host=host, port=port, log_level="info", reload=True)

@click.group(chain=True, invoke_without_command=True)
@click.pass_context
def msys(ctx):
    if ctx.invoked_subcommand is None:
        launch()

@msys.command("serve")
@click.option('-m', '--module', default="msys.scripts.msys:server", help='The module to host.')
@click.option('-h', '--host', default="127.0.0.1", help='The host address.', type=str)
@click.option('-p', '--port', default=8000, help='The port address.', type=int)
def serve(module, host, port):
    """launches costom server"""
    launch(module, host, port)

@msys.command("modules")
def modules():
    """lists registered modules"""
    print("Registered Modules:")
    modules = get_modules()
    for m in modules:
        print(m)

@msys.command("types")
def types():
    """lists registered types"""
    print("Registered Types:")
    types = get_types()
    for t in types:
        print(t)

@msys.command("extensions")
def extensions():
    """lists registered extensions"""
    print("Registered Extensions:")
    extensions = get_extensions()
    for e in extensions:
        print(e)

if __name__ == '__main__':
    msys()