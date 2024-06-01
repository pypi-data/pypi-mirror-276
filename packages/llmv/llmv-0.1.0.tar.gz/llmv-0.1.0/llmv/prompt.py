import base64
import os
import subprocess

import cv2


"""
Overview:
---------
This module provides various utilities for processing images and videos, including resizing images, extracting audio from videos, and encoding images and frames to base64. It also provides functions for generating chat prompt messages with these media contents. 

Key Functions:
--------------
1. `resize_images(images, size="1024x1024")`:
   - Resizes a list of image files to a specified size and saves the resized images in a 'resized' directory.

2. `extract_audio_from_video(video_path)`:
   - Extracts audio from a given video file using ffmpeg and saves it as an MP3 file.

3. `read_one_frame_per_second(video_path)`:
   - Reads one frame per second from a given video file, resizes these frames to 512x512 pixels, and encodes them to base64.

4. `base_64_image(b64_data)` and `image_content(images)`:
   - Encodes image data to base64 and wraps it in a dictionary format suitable for prompt generation.

5. `wrap_system_prompt(prompt)`:
   - Wraps a given prompt in a dictionary structure with a 'system' role.

6. `wrap_prompt(prompt, images)`:
   - Wraps a prompt and a list of images in a suitable format for chat messages, encoding the images in base64.

7. `wrap_messages(user, assistant)`:
   - Wraps user and assistant messages together in a list of dictionaries.

8. `assistant_response(text)`:
   - Wraps an assistant's response in a dictionary format.

9. `video_prompt_messages(prompt, video_path)`:
   - Generates prompt messages for a given video, including reading frames per second from the video and encoding them in base64 along with an additional description.

Usage:
------
The utilities provided in this module can be used to preprocess images and videos, and then generate appropriate prompt messages for chat applications or other interaction-based systems. 
Import necessary functions from the module and call them with appropriate arguments as required.
"""

def read_image_as_b64(image_path):
    # try to read image_path and encode as base64 if fails check if iamge_path is already base64 encoded and return it
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except:
            return image_path

def base_64_image(b64_data):
    return f"data:image/jpeg;base64,{b64_data}"


def image_content(images):
    return [
        {"type": "image_url", "image_url": base_64_image(image)} for image in images
    ]


# return [[{"type": "image_url", "image_url": {"url": image}}] for image in images]


def wrap_system_prompt(prompt):
    if not prompt:
        return []
    return [
        {
            "role": "system",
            "content": prompt,
        },
    ]

def resize_images(images, size="1024x1024"):
    if not images:
        return []
    
    os.makedirs("resized", exist_ok=True)
    resized = []
    for image in images:
        resized_img = os.path.join("resized", os.path.basename(image))
        process = subprocess.Popen(
            f"convert {image} -resize {size} {resized_img}".split(" ")
        )
        process.wait()
        resized.append(resized_img)
        # os.remove(resized)
    return resized

def wrap_prompt(prompt, images):
    messages = [
        {
            "role": "user",
            "content": prompt,
        },
    ]

    if images and len(images) > 0:
        base64_images = [read_image_as_b64(image) for image in images]
        messages.append(
            {
                "role": "user",
                "content": image_content(base64_images),
            }
        )
        
    return messages


def wrap_messages(user, assistant):
    return [
        {
            "role": "user",
            "content": user,
        },
        {
            "role": "assistant",
            "content": assistant,
        },
    ]


def assistant_response(text):
    return [{"role": "assistant", "content": text}]



def extract_audio_from_video(video_path):
    """
    Extracts audio from a video file using ffmpeg and saves it as an MP3 file.

    Parameters:
    video_path (str): The path to the video file.
    """
    output_audio_path = "tmp.mp3"
    try:
        # Command to extract audio using ffmpeg
        command = ['ffmpeg', '-i', video_path, '-vn', '-acodec', 'libmp3lame', '-q:a', '2', output_audio_path]
        
        # Execute the command
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Check if the command was executed successfully
        if result.returncode == 0:
            with open(output_audio_path, "rb") as f:
                audio_data = f.read()
                return audio_data
            print(f"Audio extracted successfully and saved to {output_audio_path}")
        else:
            print(f"An error occurred: {result.stderr}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return "", str(e)

def read_one_frame_per_second(video_path):
    frame_size = (512, 512)
    # Open the video file or stream
    video = cv2.VideoCapture(video_path)
    
    # Check if video opened successfully
    if not video.isOpened():
        print("Error: Could not open video.")
        return
    
    # Get the frame rate and total frame count
    fps = video.get(cv2.CAP_PROP_FPS)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Calculate the number of frames to skip after reading one frame
    frames_to_skip = int(fps)
    
    base64Frames = []
    current_frame_number = 0
    while True:
        # Set the next frame to read
        video.set(cv2.CAP_PROP_POS_FRAMES, current_frame_number)
        
        # Read the next frame
        ret, frame = video.read()
        
        # Break the loop if there is no frame to read
        if not ret:
            break
        
        # resize the frame
        resized_frame = cv2.resize(frame, frame_size)
        # Process the frame (for example, display it)
        _, buffer = cv2.imencode(".jpeg", resized_frame)
        base64Frames.append(base64.b64encode(buffer).decode("utf-8"))
        
        # Increment the frame number by the number of frames to skip
        current_frame_number += frames_to_skip
        
        # If the next frame number exceeds the total frames, exit the loop
        if current_frame_number >= total_frames:
            break
    
    # Release the video capture object and close all OpenCV windows
    video.release()
    
    return base64Frames

def video_prompt_messages(prompt, video_path):
    # Extract audio from the video
    # audio_data = extract_audio_from_video(video_path)
    # TODO see if can send audio to llm
    # TODO when can't send audio, transcribe (whisper?) and send text to llm
    
    # Read one frame per second from the video
    base64Frames = read_one_frame_per_second(video_path)
    
    video_upload_description = "The video is uploaded as a series of frames, one frame per second."
    return wrap_prompt(prompt + video_upload_description, base64Frames)