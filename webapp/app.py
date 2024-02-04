from flask import Flask, render_template, request, send_file, jsonify
from flask_socketio import SocketIO
import subprocess
import os
import re
import time
from datetime import datetime

app = Flask(__name__)
socketio = SocketIO(app)

def get_latest_video():
    video_folder = os.path.join(os.getcwd(), 'static')
    videos = [os.path.join(video_folder, f) for f in os.listdir(video_folder) if f.endswith('.mp4')]
    if videos:
        latest_video = max(videos, key=os.path.getmtime)
        return latest_video
    else:
        return None
    
def get_folder_list():
    images_path = "../images/"  # Adjust the path as needed
    folder_list = []

    try:
        # List all directories in the specified path
        folders = [f for f in os.listdir(images_path) if os.path.isdir(os.path.join(images_path, f))]
        
        # Sort the folders by name (assuming the date strings are formatted in a way that sorting them alphabetically also sorts them chronologically)
        folder_list = sorted(folders, reverse=True)

    except FileNotFoundError:
        print(f"Error: Path '{images_path}' not found.")
    
    return folder_list

@socketio.on('progress_update')
def handle_progress_update(progress):
    socketio.emit('update_progress', {'progress': progress})

@socketio.on('time_remaining_update')
def handle_time_remaining_update(time_remaining):
    socketio.emit('update_time_remaining', {'time_remaining': time_remaining})

@app.route('/', methods=['GET'])
def index():
    # Get the latest video filename
    latest_video = get_latest_video()
    folder_list = get_folder_list() 
    return render_template('index.html', latest_video=latest_video, folder_list=folder_list)

@app.route('/video')
def video():
    latest_video = get_latest_video()
    if latest_video:
        return send_file(latest_video, as_attachment=True)
    else:
        return "No video available."

@app.route('/create_timelapse', methods=['POST'])
def create_timelapse():
    selected_date = request.form.get('selected_date')  # Get the selected date from the form data
    print("data" + selected_date)
    timestamp = selected_date if selected_date else datetime.now().strftime("%Y_%m_%d")
    process = subprocess.Popen(['python', '../script/createTimelaps.py', '../images/' + timestamp + '/', 'static/'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    
    start_time = time.time()
    progress = 0
    while True:
        output_line = process.stdout.readline()
        if output_line == '' and process.poll() is not None:
            break
        if output_line:
            match = re.search(r'Progress: (\d+\.\d+)%', output_line)
            if match:
                progress = float(match.group(1))
                socketio.emit('update_progress', {'progress': progress})

            elapsed_time = time.time() - start_time

            # Check if progress is greater than zero before calculating time_per_frame
            if progress > 0:
                time_per_frame = elapsed_time / (progress / 100)
                remaining_time = (100 - progress) / 100 * time_per_frame
            else:
                time_per_frame = 0
                remaining_time = 0

            socketio.emit('update_time_remaining', {'time_remaining': remaining_time})
    
    # Return a JSON response
    return jsonify({'message': 'Timelapse creation started.'}), 200

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, use_reloader=False, allow_unsafe_werkzeug=True)
