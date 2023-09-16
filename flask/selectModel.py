import os 
from models.converters.CycleGAN_VC2.convert import convert as CycleGAN_VC2

def selectModel(modelName, file_name, file_path, mode):
    """ 引数modelNameのモデルに音声の変換を行なってもらうメソッド

    Args:
        modelName : モデルの名前
        file_name : 音声のファイル名
        file_path : 変換前の音声のパス
        mode : convertM2W if male -> female else convertW2M

    """

    if modelName == "CycleGAN_VC2":
        os.chdir(f"./models/converters/{modelName}/")
        os.system(f"poetry run python3 convert.py --file_name {file_name} --file_path {file_path} --mode {mode}")
        os.chdir(f"../../../")
        print(os.curdir)
    