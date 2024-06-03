# hello_world/cli.py

import click
from deshi_hello_world import hello, multiply

@click.command()
@click.option('--greet', is_flag=True, help='Invoke the greet command')
@click.option('--multiply', nargs=-1, type=int, help='Invoke the multiply_command with numbers')
def combined_command(greet, multiply):
    """Combined command to invoke greet and multiply_command."""
    if greet:
        click.echo(hello())
    if multiply:
        result = 1
        numbers = list(multiply)
        for num in numbers:
            result *= num
        click.echo(f"The result of {' * '.join(map(str, numbers))} is {result}")

if __name__ == '__main__':
    combined_command()
