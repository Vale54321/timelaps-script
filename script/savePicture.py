import cv2
import os
from datetime import datetime
import schedule
import time
import sys

def save_image_from_rtsp(rtsp_url, output_path):
    # Open the RTSP stream
    cap = cv2.VideoCapture(rtsp_url)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open RTSP stream.")
        return

    # Read a frame from the RTSP stream
    ret, frame = cap.read()

    # Check if the frame was read successfully
    if not ret:
        print("Error: Could not read frame from RTSP stream.")
        return
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Resize the frame to Full HD resolution (1920 x 1080)
    frame = cv2.resize(frame, (1920, 1080))

    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    # Save the resized frame as an image
    image_filename = f"image_{timestamp}.jpg"
    cv2.imwrite(os.path.join(output_path, image_filename), frame)

    # Release the camera capture object
    cap.release()

    return output_path + "/" + image_filename

def job():
    # Set your RTSP URL and output path
    rtsp_url = "rtsps://10.20.30.1:7441/mstHSxlikG8CrMfh?enableSrtp"
    timestamp = datetime.now().strftime("%Y_%m_%d")
    output_path = "../images/" + timestamp + "/"  # Replace with your desired output path

    # Save an image from the RTSP stream
    image_filename = save_image_from_rtsp(rtsp_url, output_path)
    if image_filename:
        print(f"{os.getcwd()}/{__file__} -> created {image_filename}")
        sys.stdout.flush()  # Flush the standard output buffer

if __name__ == "__main__":
    print("Start Picture Saving")
    job()
    # Schedule the job to run every 30 seconds
    schedule.every(30).seconds.do(job)

    # Run the scheduler continuously
    while True:
        schedule.run_pending()
        time.sleep(1)  # Sleep for a short duration to avoid high CPU usage
