import click
from meghana_hello_world import hello, sum_numbers

@click.group()
def cli():
    pass

@cli.command()
def greet():
    """Simple program that greets the user."""
    click.echo(hello())

@cli.command()
@click.argument('numbers', nargs=-1, type=int)
def sum_numbers_cmd(numbers):
    """Simple program that sums numbers."""
    if numbers:
        click.echo(sum_numbers(numbers))
    else:
        click.echo("No numbers provided for summing.")

if __name__ == '__main__':
    cli()
