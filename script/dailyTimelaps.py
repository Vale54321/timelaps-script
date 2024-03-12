import cv2
import os
from datetime import datetime
import schedule
import time
import subprocess

def job():
    print("Job started")
    
    # Set your RTSP URL and output path
    timestamp = datetime.now().strftime("%Y_%m_%d")
    output_path = "videos/" + timestamp + "/"  # Replace with your desired output path

    print(f"Saving image from RTSP stream to {os.getcwd() + output_path}")

    # Save an image from the RTSP stream
    subprocess.Popen(['python', 'createTimelaps.py', 'images/' + timestamp + '/', 'static/', '60'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

    print(f"Image saved at {os.getcwd() + output_path}")

    print("Job completed")

if __name__ == "__main__":
    print("main started")
    # Schedule the job to run every 30 seconds
    # schedule.every(30).minutes.do(job)
    job()
    # Run the scheduler continuously
    # while True:
    #             # Print the next scheduled run time
    #     next_run = schedule.next_run()
    #     print(f"Next run scheduled at: {next_run}")

    #     schedule.run_pending()
    #     time.sleep(5)  # Sleep for a short duration to avoid high CPU usage
