import cv2
import os
from datetime import datetime

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
    
    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")

    # Save the frame as an image
    cv2.imwrite(f"{output_path}image_{timestamp}.jpg", frame)

    # Release the camera capture object
    cap.release()

if __name__ == "__main__":
    # Set your RTSP URL and output path
    rtsp_url = "rtsps://192.168.1.1:7441/exQBgfl7iPoNRAfs?enableSrtp"
    output_path = "images/"  # Replace with your desired output path

    # Save an image from the RTSP stream
    save_image_from_rtsp(rtsp_url, output_path)
    print(f"Image saved at {os.getcwd() + output_path}")
