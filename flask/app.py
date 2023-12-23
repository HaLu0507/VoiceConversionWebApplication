# coding: UTF-8
from flask import Flask, render_template, request, send_from_directory, jsonify
import os 
from selectModel import selectModel
from models.preprocess.removalNoise import removalBackgroundNoise
from makeSps import saveSps

app = Flask(__name__)

count = 0

def convertWav(file_name):
    """ ユーザから得られた音声データをwav形式に変換するメソッド

    Args:
        file_name : 拡張子付きの音声データのファイル名

    Returns: 拡張子をwavにしたファイル名
    """
    os.system(f"ffmpeg -y -i ./audio/origin/{file_name} ./audio/origin/{file_name.split('.')[0]}.wav")

#音声をhtmlに送信するメソッド
@app.route("/audio/<path:filename>")
def play_before(filename):
    #第一引数が取得したいファイルのディレクトリ名、
    #第二引数が取得したいファイルのファイル名
    return send_from_directory("audio", filename)


#画像をhtmlに送信するメソッド
@app.route("/sps/<path:filename>")
def show_mel_converted(filename):
    #第一引数が取得したいファイルのディレクトリ名、
    #第二引数が取得したいファイルのファイル名
    return send_from_directory("sps", filename)


#最初の画面の表示
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('login.html')

#パスワード認証
@app.route('/login', methods=['GET', 'POST'])
def modeSelect():
    # フォームから送信されたユーザー名とパスワードを取得
    try:
        entered_password = request.form['data1']
        if(not entered_password == "webApp2023"):
            return render_template('login.html')
        else:
            return render_template('modeSelect.html')

    except:
        return render_template('login.html')


#
#音声変換方法のモードの選択
#

#音声ファイルで変換
@app.route('/modeFile', methods=['GET', 'POST'])
def modeFile():
    print("file")
    return render_template('post.html',boolean = False)



#音声を録音して変換
@app.route('/modeRecord', methods=['GET', 'POST'])
def modeRecord():
    print("record")
    return render_template('post.html',boolean = False)



#MOSモード
@app.route('/modeMOS', methods=['GET', 'POST'])
def modeMos():
    print("mos")
    return render_template('mos.html',boolean = False)

#音声ファイルを取得し変換するメソッド
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
        
    #変換が男性から女性か女性から男性かの文字列
    #男性から女性:"convertM2W",  女性から男性:"convertW2M"
    mode = request.form.get('sel')

    #変換の手法の文字列
    #CycleGAN_VC2、MaskCycleGAN_VC
    method = request.form.get('method')

    print(method)
    #htmlでアップロードされたファイルを取得
    file = request.files['file']
    print(request.files['file'])


    #保存先のファイル名を指定(拡張子なし)
    origin_name = str(file.filename).split('.')[0]

    #ファイルを選択しなかったときの処理
    if origin_name == "":
        return render_template('post.html',error = "ファイルを選択してください",boolean = False)
    
    #modeを何も選択しなかったときの処理
    if mode == None:
        return render_template('post.html', error="変換方法を選択してください",boolean = False)
    

    #保存先の絶対パスとファイル名を指定
    origin_path = os.path.join(os.getcwd(), 'audio/origin/', file.filename)
    #指定した形式で保存
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


#
#MOSのモードの選択
#

#Naturalness
@app.route('/NaturalnessMOS', methods=['GET', 'POST'])
def naturalnessMOS():
    print("mos")
    return render_template('mos.html',boolean = False)


#Similarity
@app.route('/SimilarityMOS', methods=['GET', 'POST'])
def similarityMos():
    return render_template('mos.html',boolean = False)


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=5000)
