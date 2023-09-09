from flask import Flask, render_template, request, send_from_directory
import os 
from models.converters.CycleGAN_VC2.convert import convert

app = Flask(__name__)

#変換前のファイルの名前
file_name_before = ""
#変換後のファイルの名前
file_name_after = ""


#最初の画面の表示
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('sample.html')

#音声を再生するためのメソッド？
@app.route('/beforeMusic')
def play_music_before():
    global file_name_before

    #第一引数が取得したいファイルのディレクトリ名、
    #第二引数が取得したいファイルのファイル名
    return send_from_directory("music", file_name_before)

#音声を再生するためのメソッド？
@app.route('/afterMusic')
def play_music_after():
    global file_name_after

    #第一引数が取得したいファイルのディレクトリ名、
    #第二引数が取得したいファイルのファイル名
    return send_from_directory("music", file_name_after)

#音声ファイルを取得するメソッド
@app.route('/second', methods=['GET', 'POST'])
def upload_file():
    #htmlでアップロードされたファイルを取得
    file = request.files['file']

    #保存先のファイル名を指定
    global file_name_before
    file_name_before = str(file.filename)

    if file_name_before == "":
        return render_template('sample.html')
    #保存先のパスとファイル名を指定
    file_path = os.path.join('./music/', file.filename)

    #指定した形式で保存
    file.save(file_path)

    #変換後の音声
    global file_name_after
    file_name_after = str(file.filename)

    convert(file_name=file_name_before, file_path=file_path)

    #次の外面に遷移する
    #nameはファイルのパス
    return render_template('post.html',name = file_path)

if __name__ == "__main__":
    app.run(debug=True)