from flask import Flask, render_template, request, send_from_directory
import os 

app = Flask(__name__)

#最初の画面の表示
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('sample.html')

#音声を再生するためのメソッド？
@app.route("/music/sampleAudio.m4a")
def play_music():
    return send_from_directory("music", "sampleAudio.m4a")

#音声ファイルを取得するメソッド
@app.route('/second', methods=['GET', 'POST'])
def upload_file():
    #htmlでアップロードされたファイルを取得
    file = request.files['file']
    #保存先のパスとファイル名を指定
    file_path = os.path.join('./music/', file.filename)
    #指定した形式で保存
    file.save(file_path)
    #次の外面に遷移する
    #nameはファイルのパス
    return render_template('post.html',name = file_path)

if __name__ == "__main__":
    app.run(debug=True)