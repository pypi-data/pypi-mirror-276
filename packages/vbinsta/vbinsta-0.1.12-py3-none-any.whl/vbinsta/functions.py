from instagrapi import Client
import os
import json
from PIL import Image


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


def get_user_info(username: str) -> dict:
    pass


def upload_single_image(client: Client, path: str, caption: str) -> dict:
    """
    Uploads a single image to Instagram.

    Args:
        client (Client): The Instagram client object.
        path (str): The path to the image file.
        caption (str): The caption for the image.

    Returns:
        dict: A dictionary containing the response from the Instagram API.
    """
    client.photo_upload(path, caption)


def upload_carousel(client: Client, paths: list, caption: str) -> dict:
    """
    Uploads a carousel of images to Instagram.

    Args:
        client (Client): The Instagram client object.
        paths (list): A list of file paths of the images to be uploaded.
        caption (str): The caption for the carousel.

    Returns:
        dict: A dictionary containing the response from the Instagram API.

    """
    client.album_upload(paths, caption)


def resize_images(images: list, size: tuple) -> list:
    """
    Resizes a list of images to the specified size.

    Args:
        images (list): A list of image file paths.
        size (tuple): The target size in pixels (width, height).

    Returns:
        list: A list of resized image file paths.

    """
    resized_images = []
    for image_path in images:
        with Image.open(image_path) as img:
            resized_img = img.resize(size)
            resized_path = f"resized_{os.path.basename(image_path)}"
            resized_img.save(resized_path)
            resized_images.append(resized_path)
    return resized_images


def fetch_posts_info(client, no_of_posts):
    # Get the last 5 media posts
    medias = client.user_medias(client.user_id, amount=no_of_posts)

    for media in medias:
        # Get detailed information about the media post
        media_info = client.media_info(media.id)

        print(f"Post ID: {media_info.id}")
        print(f"Caption: {media_info.caption_text}")
        print(f"Likes: {media_info.like_count}")
        # Shares information is not directly available
        print("Comments:")

        # Get the comments for the media post
        comments = client.media_comments(media.id)

        for comment in comments:
            print(f"{comment.user.username}: {comment.text}")

        print("\n")
