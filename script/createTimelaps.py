import cv2
import os
from datetime import datetime

def create_video(images_folder, output_video_path, fps=60, x=1920, y=1080):
    # Get a list of all image files in the folder
    image_files = [f for f in os.listdir(images_folder) if f.endswith(".jpg")]

    # Initialize the video writer
    # Initialize the video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (x, y))


    # Loop through all image files
    for image_file in image_files:
        image_path = os.path.join(images_folder, image_file)

        # Read the image
        image = cv2.imread(image_path)

        # Check if the image exists
        if image is not None:
            # Resize the image if needed
            image = cv2.resize(image, (x, y))  # Uncomment and adjust if necessary

            # Write the image to the video
            video_writer.write(image)

    # Release the video writer
    video_writer.release()
    