import click

import processors


@click.group()
def cli():
    pass


@click.command()
@click.option('-v', '--val', help='Provide a value to echo')
def echo(val):
    click.echo(f"Input:\t{val}")


@click.command()
@click.option(
    '-s',
    '--structure', 
    default='df', 
    type=click.Choice(['df', 'dict', 'matrix', 'all'], case_sensitive=False), 
    help='Aggregate flight legs using data structure specified. If `all`, utility will return each option sequentially without limits')
@click.option('--num', default=10, type=int, help='Specify number of row to print to console, sorted descending')
@click.option('--matrix-headers', default=True, type=bool, help='Boolean flag to include column/ row headers in matrix. Only applies to matrix')
def flight_legs(structure, num):
    handler = {
        'df': processors.aggregate_df, 
        'dict': processors.aggregate_dict,
        'matrix': processors.process_matrix
    }
    if structure == 'all':
        for key in handler:
            click.echo('-' * 10)
            click.echo(key)
            click.echo(handler.get(key)())
        return 

    func = handler.get(structure)
    if structure == 'df':
        click.echo(func().head(num))
    else:
        click.echo(func()[:num])


@click.option('-i', '--index', type=int, help='Provided an index, lookup the airport name from the matrix')
def airport_from_index(idx):
    code = processors.index_to_destination_airport(idx)
    if not code:
        click.echo('No airport found. Are you sure the index is correct?')
    else:
        click.echo(f'Airport found:\t{code}')


if __name__ == '__main__':

    cli.add_command(echo)
    cli.add_command(flight_legs)

    cli()