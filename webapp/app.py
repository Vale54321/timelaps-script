from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        rtsp_url = request.form['rtsp_url']
        output_path = request.form['output_path']

        # Call your Python script using a subprocess
        subprocess.run(['python', 'capture_image.py', rtsp_url, output_path])

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)