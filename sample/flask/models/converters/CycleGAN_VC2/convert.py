from .Generator import Generator
import torch
import librosa 
from . import preprocess
import numpy as np
import os 
import soundfile as sf

def convert(file_name, file_path):
    """ 引数で与えられた音声ファイルを変換し, 変換した音声ファイルを保存するメソッド

    Args:
        file_path : 変換前の音声のパス
    """

    # 変換した音声を保存するディレクトリ
    # app.py から見た時の相対パスになっている
    out_dir = "./music/converted_" 

    # モデルの生成
    generatorF2M = Generator().to('cpu')
    generatorM2F = Generator().to('cpu')
    hub_vocoder = torch.hub.load('descriptinc/melgan-neurips', 'load_melgan', model_name='multi_speaker')

    # モデルのチェックポイントをロードする
    checkPoint = torch.load("./models/converters/CycleGAN_VC2/_CycleGAN_CheckPoint", torch.device('cpu'))
    generatorF2M.load_state_dict(
        state_dict=checkPoint['model_genA2B_state_dict'])
    generatorM2F.load_state_dict(
        state_dict=checkPoint['model_genB2A_state_dict'])
    
    # 前処理
    # hyper parameters
    n_mel_channels = 80
    sampling_rate = 22050 # default : 16000
    frame_period = 5.0

    print(f"file path : {file_path}")
    wav, _ = librosa.load(file_path, sr=sampling_rate, mono=True)
    wav = preprocess.wav_padding(wav=wav,
                                    sr=sampling_rate,
                                    frame_period=frame_period,
                                    multiple=4)
    
    # tensor に変換し, 型を(1,Time)に変換する
    wav = torch.from_numpy(wav).float()
    wav = wav.unsqueeze(0)
    # numpy に型を戻す
    wav = wav.to('cpu').detach().numpy().copy()
    
    # getting data B mel spectrogram
    mel_sp = preprocess.melGAN_decompose(wav, n_mel_channels) # 入力が(1,Time)の音声しか無理な点に注意
    mel_sp_transposed = mel_sp.T
    mel_sp_norm = np.array([mel_sp_transposed])
    mel_sp_norm = torch.from_numpy(mel_sp_norm).float()

    # convert , output: (batch size, Hz, time)
    mel_sp_converted_norm = generatorM2F(mel_sp_norm)

    # mel sp -> wav
    # input  : tensor(batch size, Hz=80, time)
    # output : tensor(batch size, time)
    wav_transformed = hub_vocoder.inverse(mel_sp_converted_norm) 
    wav_transformed = wav_transformed.squeeze(0) # wav_transformed (time)
    wav_transformed = wav_transformed.to('cpu').detach().numpy().copy() # tensor to numpy
    
    # librosa の output 関数はなかったので, wavファイルへの変換は soundfile モジュールを使用した
    sf.write(f"{out_dir}{file_name}",
                                wav_transformed,
                                sampling_rate,
                                subtype="PCM_24")
    
    if __name__ == '__main__':
        file_name = "sampleAudio.wav"
        file_path = "/Users/Tanaka/VoiceConversionWebApplication/sample/flask/music/sampleAudio.wav"
        print("process")
        convert(file_name, file_path)
