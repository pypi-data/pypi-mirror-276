# hello_world/cli.py
import click
from harsha_hello_world import hello

@click.command()
def greet():
    """Simple program that greets the user."""
    click.echo(hello())

if __name__ == '__main__':
    greet()
