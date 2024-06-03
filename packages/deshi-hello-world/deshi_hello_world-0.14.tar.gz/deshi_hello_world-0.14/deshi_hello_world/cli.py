# hello_world/cli.py

import click
from deshi_hello_world import hello, multiply1

@click.command()
@click.option('--greet', is_flag=True, help='Invoke the greet command')
@click.option('--multi', type=str, help='Invoke the multiply_command with numbers (comma-separated)')
def combined_command(greet, multi):
    """Combined command to invoke greet and multiply_command."""
    if greet:
        click.echo(hello())
    if multi:
        numbers = [int(num) for num in multi.split()]
        result = multiply1(*numbers)
        click.echo(f"The result of {' * '.join(map(str, numbers))} is {result}")

if __name__ == '__main__':
    combined_command()
