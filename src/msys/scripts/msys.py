import click
import uvicorn
from ..routers.server import Server


def launch(module="msys.scripts.modules:module", host= "127.0.0.1", port=8000):
    uvicorn.run(module, host=host, port=port, log_level="info", reload=True)


@click.group(chain=True, invoke_without_command=True)
@click.pass_context
def msys(ctx):
    if ctx.invoked_subcommand is None:
        launch()


@msys.command("serve")
@click.option('-m', '--module', default="msys.scripts.modules:module", help='The module to host.')
@click.option('-h', '--host', default="127.0.0.1", help='The host address.', type=str)
@click.option('-p', '--port', default=8000, help='The port address.', type=int)
def serve(module, host, port):
    """launches costom server"""
    launch(module, host, port)


if __name__ == '__main__':
    msys()