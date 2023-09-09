from flask import Flask, render_template, request, send_from_directory
import os 

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('sample.html')

@app.route("/music/sampleAudio.m4a")
def play_music():
    return send_from_directory("music", "sampleAudio.m4a")

@app.route('/second', methods=['GET', 'POST'])
def upload_file():
    file = request.files['file']
    file_path = os.path.join('./music/', file.filename)
    file.save(file_path)
    return render_template('post.html',name = file_path)

if __name__ == "__main__":
    app.run(debug=True)