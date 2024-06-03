
import click
from sc3dg.commands.count import count
from sc3dg.commands.model import model
from sc3dg.commands.impute import impute


@click.group()
def cli():
    pass

@click.command()
def count():
    click.echo(count())

@click.command()
def model():
    click.echo(model())

@click.command()
def impute():
    click.echo(impute())



cli.add_command(count)
cli.add_command(model)
cli.add_command(impute)

if __name__ == '__main__':
    cli()
