import click

import processor


@click.group()
def cli():
    pass


@click.command()
@click.option('--val', help='Provide a value to echo')
def echo(val):
    click.echo(f"Input:\t{val}")


@click.command()
@click.option(
    '--structure', 
    default='df', 
    type=click.Choice(['df', 'dict', 'matrix', 'all']), 
    case_sensitive=False,
    help='Aggregate flight legs using data structure specified. If `all`, utility will return each option sequentially')
@click.option('--num', default=10, type=int, help='Specify number of row to print to console, sorted descending')
def flight_legs(structure, num):
    if structure == 'df':
        airports = processor.aggregate_df()
        click.echo(airports.head(num))
    



cli.add_command(echo)
cli.add_command(flight_legs)