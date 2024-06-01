from instagrapi import Client
import os
import json

USERNAME = os.getenv('INSTA_USERNAME')
PASSWORD = os.getenv('INSTA_PASSWORD')
SESSION_FILE = os.path.expanduser("~/.vbinsta_session.json")


def save_session(client, filepath):
    """
    Save the session settings of the client to a file.

    Parameters:
    - client: The client object representing the session.
    - filepath: The path to the file where the session settings will be saved.

    Returns:
    None
    """
    with open(filepath, "w") as f:
        json.dump(client.get_settings(), f)
    print("Session saved!")


def load_session(client, filepath):
    """
    Load a session from a JSON file and set the settings for the client.

    Args:
        client (Client): The client object to set the settings for.
        filepath (str): The path to the JSON file containing the session settings.

    Returns:
        None

    Raises:
        FileNotFoundError: If the specified file does not exist.
        json.JSONDecodeError: If the JSON file is not valid.

    """
    with open(filepath, "r") as f:
        settings = json.load(f)
    client.set_settings(settings)
    print("Session loaded!")


def login(client, username, password, session_file):
    """
    Logs in the client using the provided username and password.

    Args:
        client: The client object used for making API requests.
        username: The username of the account.
        password: The password of the account.
        session_file: The file path to save the session information.

    Returns:
        None
    """
    if os.path.exists(session_file):
        load_session(client, session_file)
    else:
        CODE = input("Enter the 2FA code: ")
        client.login(username, password, verification_code=CODE)
        if client.user_id:
            print("Login successful!")
        else:
            print("Login failed.")
        save_session(client, session_file)


def LOGIN():
    client = Client()
    try:
        login(client, USERNAME, PASSWORD, SESSION_FILE)
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    if client.user_id:
        print("Login successful!: @10xphysics\n")

    return client
