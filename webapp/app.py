from flask import Flask, render_template, request, redirect, url_for, send_file
import subprocess
import os

app = Flask(__name__, static_url_path='/static')

def get_latest_video():
    video_folder = os.path.join(os.getcwd(), 'static')
    videos = [f for f in os.listdir(video_folder) if f.endswith('.mp4')]
    if videos:
        # latest_video = max(videos, key=os.path.getctime)
        return os.path.join(video_folder, videos[6])
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Call the timelapse script using a subprocess
        subprocess.run(['python', 'script/createTimelaps.py', 'webapp/static/'])
        return redirect(url_for('index'))


    # Get the latest video filename
    latest_video = get_latest_video()

    return render_template('index.html', latest_video=latest_video)

@app.route('/video')
def video():
    latest_video = get_latest_video()
    print("get video " + latest_video)
    if latest_video:
        return send_file(latest_video, as_attachment=True)
    else:
        return "No video available."


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)