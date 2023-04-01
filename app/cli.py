import click

import processors


@click.group()
def cli():
    pass


@click.command()
@click.option('--val', help='Provide a value to echo')
def echo(val):
    click.echo(f"Input:\t{val}")


@click.command()
@click.option(
    '--struct', 
    default='df', 
    type=click.Choice(['df', 'dict', 'matrix', 'all'], case_sensitive=False), 
    help='Aggregate flight legs using data structure specified. If `all`, utility will return each option sequentially without limits')
@click.option('--num', default=10, type=int, help='Specify number of row to print to console, sorted descending')
@click.option('--matrix-headers', default=True, type=bool, help='Boolean flag to include column/ row headers in matrix. Only applies to matrix')
def flight_legs(struct, num):
    handler = {
        'df': processors.aggregate_df, 
        'dict': processors.aggregate_dict,
        'matrix': processors.aggregate_matrix
    }
    if struct == 'all':
        for key in handler:
            click.echo(key)
            click.echo(handler.get(key)())
            click.echo('-' * 10)
        return 

    func = handler.get(struct)
    if struct == 'df':
        click.echo(func().head(num))
    else:
        click.echo(func()[:num])
    return    

if __name__ == '__main__':

    cli.add_command(echo)
    cli.add_command(flight_legs)

    cli()