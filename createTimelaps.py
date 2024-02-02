import cv2
import os
from datetime import datetime

def create_video(images_folder, output_video_path, fps=60, x=1920, y=1080):
    # Get a list of all image files in the folder
    image_files = [f for f in os.listdir(images_folder) if f.endswith(".jpg")]

    # Initialize the video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can change the codec as needed
    os.makedirs(os.path.dirname(output_video_path), exist_ok=True)
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (x, y))  # Adjust the resolution as needed

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

if __name__ == "__main__":
    # Set the folder containing images
    images_folder = "images"

    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")

    # Set the output video path
    output_video_path = f"videos/timelapse_{timestamp}.mp4"  # Adjust the output path as needed

    # Create the video from all images in the folder
    create_video(images_folder, output_video_path)
    print(f"Video created at {os.getcwd() + output_video_path}")
