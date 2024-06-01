from instagrapi import Client
import os
import json
from PIL import Image
import subprocess


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
    """
    Fetches information about the specified number of posts from the client's user account.

    Args:
        client: The client object representing the user account.
        no_of_posts: The number of posts to fetch information for.

    Returns:
        None
    """

    medias = client.user_medias(client.user_id, amount=no_of_posts)

    for media in medias:
        content = ""
        title = ""

        media_info = client.media_info(media.id)

        content += f"Post ID: {media_info.id}\n"
        content += f"Caption: {media_info.caption_text}\n"
        title += f"Post ID: {media_info.id}\t Likes: {media_info.like_count}\n"

        comments = client.media_comments(media.id)

        for comment in comments:
            content += f"{comment.user.username}: {comment.text}\n"

        subprocess.Popen(
            f'echo "{content}" | bat --file-name "{title}"', shell=True)
