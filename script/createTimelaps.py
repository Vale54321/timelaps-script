import cv2
import os
from datetime import datetime
import sys

def create_video(images_folder, output_video_path, fps=1, x=1920, y=1080):
    # Get a list of all image files in the folder
    image_files = [f for f in os.listdir(images_folder) if f.endswith(".jpg")]

    # Initialize the video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
    output_video_path_full = os.path.join(output_video_path, f"timelapse_{timestamp}.mp4")
    os.makedirs(os.path.dirname(output_video_path_full), exist_ok=True)
    video_writer = cv2.VideoWriter(output_video_path_full, fourcc, fps, (x, y))

    # Loop through all image files
    for image_file in image_files:
        image_path = os.path.join(images_folder, image_file)
        print(image_path)

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
    print(f"Video saved at {os.path.abspath(output_video_path_full)}")

if __name__ == "__main__":
    # Check if the command line argument for the images folder is provided
    if len(sys.argv) < 2:
        print("Usage: python createTimelaps.py <images_folder>")
        sys.exit(1)

    # Get the video folder from the command line argument
    video_folder = sys.argv[1]

    # Save an image from the RTSP stream
    create_video('../images/', video_folder)
