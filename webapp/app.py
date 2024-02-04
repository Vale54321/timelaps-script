from flask import Flask, render_template, request, send_file, jsonify
from flask_socketio import SocketIO
import subprocess
import os
import re

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

@socketio.on('progress_update')
def handle_progress_update(progress):
    socketio.emit('update_progress', {'progress': progress})

@app.route('/', methods=['GET'])
def index():
    # Get the latest video filename
    latest_video = get_latest_video()
    return render_template('index.html', latest_video=latest_video)

@app.route('/video')
def video():
    latest_video = get_latest_video()
    if latest_video:
        return send_file(latest_video, as_attachment=True)
    else:
        return "No video available."

@app.route('/create_timelapse', methods=['POST'])
def create_timelapse():
    process = subprocess.Popen(['python', '../script/createTimelaps.py', '../images/', 'static/'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    
    while True:
        output_line = process.stdout.readline()
        if output_line == '' and process.poll() is not None:
            break
        if output_line:
            match = re.search(r'Progress: (\d+\.\d+)%', output_line)
            if match:
                progress = float(match.group(1))
                socketio.emit('update_progress', {'progress': progress})

    socketio.emit('update_progress', {'progress': 100})
    
    # Return a JSON response
    return jsonify({'message': 'Timelapse creation started.'}), 200

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, use_reloader=False)
