import click
from .upload import upload
from .fetch import fetch

CONTEXT_SETTINGS = dict(
    help_option_names=[
        '-h',
        '--help'
    ],
    auto_envvar_prefix='VBINSTA'
)


@click.group(context_settings=CONTEXT_SETTINGS)
def main():
    pass


main.add_command(upload)
main.add_command(fetch)
