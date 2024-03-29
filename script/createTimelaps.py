import cv2
import os
from datetime import datetime
import sys
import time

def create_video(images_folder, output_video_path, fps=30, x=1920, y=1080):
    # Get a list of all image files in the folder
    image_files = sorted([f for f in os.listdir(images_folder) if f.endswith(".jpg")])

    # Initialize the video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
    output_video_path_full = os.path.join(output_video_path, f"timelapse_{timestamp}.mp4")
    os.makedirs(os.path.dirname(output_video_path_full), exist_ok=True)
    video_writer = cv2.VideoWriter(output_video_path_full, fourcc, fps, (x, y))

    start_time = time.time()

    # Loop through all image files
    for i, image_file in enumerate(image_files, start=1):
        image_path = os.path.join(images_folder, image_file)

        # Read the image
        image = cv2.imread(image_path)

        # Check if the image exists
        if image is not None:
            # Resize the image if needed
            image = cv2.resize(image, (x, y))
            # Write the image to the video
            video_writer.write(image)

            # Print progress and time remaining
            progress = i / len(image_files) * 100
            elapsed_time = time.time() - start_time
            time_per_frame = elapsed_time / i
            remaining_frames = len(image_files) - i
            remaining_time = remaining_frames * time_per_frame
            sys.stdout.write(f"\rProgress: {progress:.2f}% | Time Remaining: {remaining_time:.2f} seconds")
            sys.stdout.flush()

    # Release the video writer
    video_writer.release()
    
    # Print completion message
    print(f"\n{os.path.abspath(output_video_path_full)}")

if __name__ == "__main__":
    # Check if the command line argument for the images folder is provided
    if len(sys.argv) < 4:
        print("Usage: python createTimelaps.py <images_folder> <video_folder> <video_fps>")
        sys.exit(1)

    # Get the video folder from the command line argument
    images_folder = sys.argv[1]
    video_folder = sys.argv[2]
    try:
        video_fps = float(sys.argv[3])  # Convert the string to a float
    except ValueError:
        print("Error: Invalid value for video_fps. Please provide a valid float.")
        sys.exit(1)

    # Save an image from the RTSP stream
    create_video(images_folder, video_folder, fps=video_fps)
