# hello_world/cli.py

import click
from hello_world import hello, multiply

@click.command()
def greet():
    """Simple program that greets the user."""
    click.echo(hello())

@click.command()
@click.argument('a', type=int)
@click.argument('b', type=int)
def multiply_command(a, b):
    """Multiply two numbers and print the result."""
    result = multiply(a, b)
    click.echo(f"The result of {a} * {b} is {result}")

@click.group()
def cli():
    pass

cli.add_command(greet)
cli.add_command(multiply_command)

if __name__ == '__main__':
    cli()
