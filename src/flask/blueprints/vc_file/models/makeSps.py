import librosa
import numpy as np
from scipy.io import wavfile
from PIL import Image
import matplotlib.pyplot as plt
import os 

def makeSpectrogram(x, sr, frame_shift=0, n_fft=2048, isLog=True, isPower=False):
    
    if frame_shift == 0:
        frame_shift=int(sr * 0.005)
        
    # STFT
    X = librosa.stft(x.astype(np.float32), n_fft=n_fft, win_length=n_fft, hop_length=frame_shift, window="hann")
    
    # 対数振幅に変換
    # ref=np.max によりデシベルの最大値を0に正規化している
    if isLog:
        logX = librosa.amplitude_to_db(np.abs(X), ref=np.max)
    else:
        logX = X
    
    # パワースペクトルにする場合
    if isLog and isPower:
        logX = 2 * logX
    
    return logX

def saveSps(file_name):
    """ 引数に与えられたスペクトログラムの画像を生成し、保存するメソッド

    Args:
        file_name: 変換前の音声のファイル名
    """

    origin_path = f"./audio/origin/{file_name}.wav"
    converted_path = f"./audio/converted/{file_name}.wav"

    # スペクトログラムを保存するディレクトリを作成
    os.makedirs("./sps/origin/", exist_ok=True)
    os.makedirs("./sps/converted/", exist_ok=True)

    origin_sp_path = f"./sps/origin/{file_name}.jpeg"
    converted_sp_path = f"./sps/converted/{file_name}.jpeg"

    # 音声の読み込み
    sr, origin = wavfile.read(origin_path)
    sr, converted = wavfile.read(converted_path)

    # フーリエ変換により対数スペクトログラムを取得
    origin_sp = np.flip(makeSpectrogram(origin, sr), axis=0)
    converted_sp = np.flip(makeSpectrogram(converted, sr), axis=0)

    # 各ディレクトリに画像を保存する
    # Image.fromarray(origin_sp).save(origin_sp_path)
    # Image.fromarray(converted_sp).save(converted_sp_path)
    plt.imsave(origin_sp_path, origin_sp)
    plt.imsave(converted_sp_path, converted_sp)