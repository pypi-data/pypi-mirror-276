import click
from .functions import fetch_posts_info
from .login import LOGIN, RELOGIN
import requests


@click.command()
@click.option(
    "-n",
    "--no_of_posts",
    default=1,
    show_default=True,
    help="Number of posts to fetch",
)
def fetch(no_of_posts):
    client = LOGIN()
    try:
        fetch_posts_info(client, no_of_posts)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print("401 error occurred. Attempting to re-login...")
            client = RELOGIN()
            try:
                fetch_posts_info(client, no_of_posts)
            except Exception as e:
                print(f"An error occurred: {e}")
                return
        else:
            print(f"An error occurred: {e}")
            return
    except Exception as e:
        print(f"An error occurred: {e}")
        return
