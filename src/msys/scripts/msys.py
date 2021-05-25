import click
import uvicorn
from ..server import MSYSServer

server = MSYSServer()

@click.command()
@click.option('-m', '--module', default="msys.scripts.msys:server", help='The module to host.')
@click.option('-h', '--host', default="127.0.0.1", help='The host address.', type=str)
@click.option('-p', '--port', default=8000, help='The port address.', type=int)
def msys(module, host, port):
    uvicorn.run(module, host=host, port=port, log_level="info", reload=True)

if __name__ == '__main__':
    msys()