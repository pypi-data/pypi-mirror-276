import click


@click.command()
@click.option('-n', '--name', default='FlameAI', help='Name to greet')
def hey(name: str) -> None:
    """Print Hey, {name}!"""
    click.echo(click.style(f'Hey, {name}!', fg='red'))


def header(text, length=60, fill_char='='):
    """
    Print a header with given length.
    """
    text = ' ' + text + ' '
    left_len = (length - len(text)) // 2
    right_len = length - len(text) - left_len
    print(f"{left_len * fill_char}{text}{right_len * fill_char}")
