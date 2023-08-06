from tkinter import Tk, filedialog
from PIL import Image, ImageOps
from moviepy.editor import ImageClip, concatenate, AudioFileClip
import os

def select_file():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path

def resize_image(image_path, size):
    image = Image.open(image_path).convert("RGB")  # Convert to RGB mode
    image = ImageOps.fit(image, size, method=Image.BICUBIC)
    resized_image_path = os.path.splitext(image_path)[0] + "_resized.jpg"
    image.save(resized_image_path)
    return resized_image_path

def select_output_path():
    root = Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(defaultextension=".mp4")
    return file_path

def create_video():
    # Select the image file
    print("Select the image file:")
    image_path = select_file()

    # Check if the image file exists
    if not os.path.exists(image_path):
        print("Image file not found.")
        return

    # Select the audio file
    print("Select the audio file:")
    audio_path = select_file()

    # Check if the audio file exists
    if not os.path.exists(audio_path):
        print("Audio file not found.")
        return

    # Select the output video file location
    print("Select the output video file location:")
    output_path = select_output_path()

    try:
        # Resize the image
        resized_image_path = resize_image(image_path, (800, 800))

        # Load the image
        image = ImageClip(resized_image_path)

        # Load the audio file
        audio_clip = AudioFileClip(audio_path)

        # Set the audio for the image clip
        image_clip = image.set_audio(audio_clip)

        # Set the duration of the video equal to the audio duration
        video_duration = audio_clip.duration
        image_clip = image_clip.set_duration(video_duration)

        # Set the frames per second (fps) for the video clip
        fps = 12  # Adjust the desired frames per second
        image_clip = image_clip.set_fps(fps)

        # Save the video
        image_clip.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=fps)
        print("Video saved successfully at:", output_path)

        # Remove the temporary file
        os.remove(resized_image_path)

    except Exception as e:
        print("An error occurred:", str(e))

# Call the function to create the video
create_video()
