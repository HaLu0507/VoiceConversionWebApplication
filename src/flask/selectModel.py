import os 

def selectModel(modelName, origin_path, mode):
    """ 引数modelNameのモデルに音声の変換を行なってもらうメソッド

    Args:
        modelName : モデルの名前
        origin_path : 変換前の音声のパス(拡張子付き)
        mode : convertM2W if male -> female else convertW2M

    """

    # モデルがあるディレクトリに移動
    os.chdir(f"./models/converters/{modelName}/")
    # 変換を行う
    os.system(f"poetry run python3 convert.py --origin_path {origin_path} --mode {mode}")
    # 元のディレクトリに戻る
    os.chdir(f"../../../")