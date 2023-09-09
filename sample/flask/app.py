from flask import Flask, render_template, request
import os 

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('sample.html')

@app.route('/second', methods=['GET', 'POST'])
def upload_file():
    file = request.files['file']
    file_path = os.path.join('./', file.filename)
    file.save(file_path)
    return render_template('post.html',name = (file.filename))

if __name__ == "__main__":
    app.run(debug=True)