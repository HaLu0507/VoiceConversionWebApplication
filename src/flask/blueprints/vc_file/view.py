from flask import Blueprint, render_template, send_from_directory, request
from .models.selectModel import selectModel
from .models.preprocess.removalNoise import removalBackgroundNoise
from .models.makeSps import saveSps

import os

vc_file = Blueprint('vc_file', __name__, template_folder='vc_file_templates')

def convertWav(file_name):
    """ ユーザから得られた音声データをwav形式に変換するメソッド

    Args:
        file_name : 拡張子付きの音声データのファイル名

    Returns: 拡張子をwavにしたファイル名
    """
    os.system(f"ffmpeg -y -i ./audio/origin/{file_name} ./audio/origin/{file_name.split('.')[0]}.wav")

#音声をhtmlに送信するメソッド
@vc_file.route("/audio/<path:filename>")
def play_before(filename):
    #第一引数が取得したいファイルのディレクトリ名、
    #第二引数が取得したいファイルのファイル名
    return send_from_directory("audio", filename)


#画像をhtmlに送信するメソッド
@vc_file.route("/sps/<path:filename>")
def show_mel_converted(filename):
    #第一引数が取得したいファイルのディレクトリ名、
    #第二引数が取得したいファイルのファイル名
    return send_from_directory("sps", filename)

#音声ファイルを取得し変換するメソッド
@vc_file.route('/upload', methods=['GET', 'POST'])
def upload_file():
    try:
        #変換が男性から女性か女性から男性かの文字列
        #男性から女性:"convertM2W",  女性から男性:"convertW2M"
        mode = request.form.get('sel')

        #変換の手法の文字列
        #CycleGAN_VC2、MaskCycleGAN_VC
        method = request.form.get('method')

        print(method)
        #htmlでアップロードされたファイルを取得
        file = request.files['file']
    except:
        return render_template('post.html',error = "正しくアクセスしてください",boolean = False)
    print(request.files['file'])


    #保存先のファイル名を指定(拡張子なし)
    origin_name = str(file.filename).split('.')[0]

    #ファイルを選択しなかったときの処理
    if origin_name == "":
        return render_template('post.html',error = "ファイルを選択してください",boolean = False)
    
    #modeを何も選択しなかったときの処理
    if mode == None:
        return render_template('post.html', error="変換方法を選択してください",boolean = False)
    
    # もしディレクトリがない場合、ディレクトリを作成
    os.makedirs(os.path.join(os.getcwd(), 'audio/origin/'), exist_ok=True)
    os.makedirs(os.path.join(os.getcwd(), 'audio/converted/'), exist_ok=True)

    # 保存先の絶対パスとファイル名を指定
    origin_path = os.path.join(os.getcwd(), 'audio/origin/', file.filename)
    # 指定した形式で保存
    file.save(origin_path)

    if file.filename.split('.')[-1] != "wav": # 拡張子がwavでない場合は変換する
        convertWav(file.filename)

    # 参照するパスとファイル名を変更
    origin_path = os.path.join(os.getcwd(), f"audio/origin/{origin_name}.wav")

    # ユーザがアップロードした音声の背景ノイズを除去する
    removalBackgroundNoise(origin_path)

    # 音声変換
    selectModel(modelName=method, origin_path=origin_path, mode=mode)

    # スペクトログラムの画像を求める
    saveSps(origin_name)

    #次の外面に遷移する
    #fileBは変換前の音声ファイル、fileAは変換後の音声ファイル
    return render_template('post.html', file_name=str(origin_name), boolean=True)