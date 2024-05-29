import os
import random
import typing
from moviepy.editor import VideoFileClip
from PIL import Image


def create_thumbnail(video_path, output_path, time_sec=lambda x: random.randint(0, x)):
    """
    Creates a thumbnail for a video at the specified time.

    Args:
    video_path (str): Path to the video file.
    time_sec (float): Time in seconds to extract the thumbnail.
    output_path (str): Path to save the thumbnail image.
    """
    # Load the video file
    clip = VideoFileClip(video_path)

    # Get the frame at the specified time
    if isinstance(time_sec, int):
        time_sec = float(time_sec)
    else:
        time_sec = time_sec(clip.duration)

    frame = clip.get_frame(time_sec)

    # Save the frame as an image
    image = Image.fromarray(frame)
    image.save(output_path)


def batch_thumbnails(
    folder_path,
    thumbnail_folder_path = None,
    supported_extensions: typing.List[str] = [".mp4", ".mkv", ".mov", ".avi", ".webm"],
    time_sec=lambda x: random.randint(0, x),
):
    """
    Generate thumbnails for all video files in the given folder and save them in the specified thumbnail folder.

    Args:
        folder_path (str): The path to the folder containing the video files.
        thumbnail_folder_path (str, optional): The path to the folder where the thumbnails will be saved. If not provided, the thumbnails will be saved in the same folder as the videos. Defaults to None.
        supported_extensions (List[str], optional): The list of supported video file extensions. Defaults to [".mp4", ".mkv", ".mov", ".avi", ".webm"].
        time_sec (Callable[[float], int], optional): A function that takes the duration of a video in seconds and returns the time in seconds to extract the thumbnail. Defaults to a function that randomly selects a time between 0 and the video duration.

    Returns:
        None
    """
    os.makedirs(folder_path, exist_ok=True)

    if thumbnail_folder_path:
        os.makedirs(thumbnail_folder_path, exist_ok=True)
    else:
        thumbnail_folder_path = folder_path

    for file in os.listdir(folder_path):
        file : str
        if file.endswith(tuple(supported_extensions)):
            video_path = os.path.join(folder_path, file)
            output_path = os.path.join(thumbnail_folder_path, file)
            create_thumbnail(video_path, output_path, time_sec)


