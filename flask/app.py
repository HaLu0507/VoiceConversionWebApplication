from flask import Flask, render_template, request, send_from_directory
import os 
from models.converters.CycleGAN_VC2.convert import convert

app = Flask(__name__)


def convertExt(file_name):
    """ ユーザから得られた音声データの拡張子をwavに変更するメソッド

    Args:
        file_name : 音声データのファイル名

    Returns: 拡張子をwavにしたファイル名
    """

    # 拡張子を取り出す
    ext = file_name.split('.')[-1]
    print(f"拡張子 : {ext}")
    # ファイル名を取り出す
    name = file_name.split('.')[0]
    print(f"ファイル名 : {name}")
    # 音声ファイルがあるディレクトリ
    path = "./music"
    print(f"パス : {path}")

    if ext != "wav": # wav 以外
        os.system(f"afconvert -f WAVE -d LEI24 {path}/{name}.{ext} {path}/{name}.wav")

    return f"{name}.wav"



#音声をhtmlに送信するメソッド
@app.route("/music/<path:filename>")
def play_before(filename):
    #第一引数が取得したいファイルのディレクトリ名、
    #第二引数が取得したいファイルのファイル名
    return send_from_directory("music", filename)


#最初の画面の表示
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('sample.html')


#音声ファイルを取得するメソッド
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    #変換が男性から女性か女性から男性かの文字列
    mode = request.form.get('sel')
    print(mode)
    
    #htmlでアップロードされたファイルを取得
    file = request.files['file']

    #保存先のファイル名を指定
    file_name_before = str(file.filename)

    if file_name_before == "":
        return render_template('sample.html')
    
    #保存先のパスとファイル名を指定
    file_path = os.path.join('./music/', file.filename)
    #指定した形式で保存
    file.save(file_path)

    # 拡張子の変更
    file_name_before = convertExt(file_name_before)
    # 参照するパスとファイル名を変更
    file_path = os.path.join('./music/', file_name_before)

    #変換後の音声の名前
    file_name_after = str(file.filename).split(".")[0]
    file_name_after = "converted_" + str(file_name_after) +".wav"

    #音声変換
    convert(file_name=file_name_before, file_path=file_path)

    #次の外面に遷移する
    #fileBは変換前の音声ファイル、fileAは変換後の音声ファイル
    return render_template('post.html', fileB = str(file_name_before), fileA = str(file_name_after))



if __name__ == "__main__":
    app.run(debug=True)