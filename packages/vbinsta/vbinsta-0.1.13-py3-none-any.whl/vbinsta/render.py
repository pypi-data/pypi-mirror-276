import click


@click.command()
@click.option(
    "-t",
    "--topic",
    default=5,
    show_default=True,
    help="Number of posts to fetch",
)
def render(topic):
    pass
