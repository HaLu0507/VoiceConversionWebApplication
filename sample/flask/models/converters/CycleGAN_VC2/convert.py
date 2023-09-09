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
    out_dir = f"./music/converted_{file_name}"

    # モデルの生成
    generatorF2M = Generator().to('cpu')
    generatorM2F = Generator().to('cpu')
    hub_vocoder = torch.hub.load('descriptinc/melgan-neurips', 'load_melgan', model_name='multi_speaker')

    # モデルのチェックポイントをロードする
    checkPoint = torch.load(file_path)
    generatorF2M.load_state_dict(
        state_dict=checkPoint['model_genA2B_state_dict'])
    generatorM2F.load_state_dict(
        state_dict=checkPoint['model_genB2A_state_dict'])
    
    # 前処理
    # hyper parameters
    n_mel_channels = 80
    sampling_rate = 22050 # default : 16000
    frame_period = 5.0

    wav, _ = librosa.load(file_path, sr=sampling_rate, mono=True)
    wav = preprocess.wav_padding(wav=wav,
                                    sr=sampling_rate,
                                    frame_period=frame_period,
                                    multiple=4)
    
    # getting data B mel spectrogram
    mel_sp = preprocess.melGAN_decompose(wav, n_mel_channels) 
    mel_sp_transposed = mel_sp.T
    mel_sp_norm = torch.from_numpy(mel_sp_transposed).float()

    # convert , output: (batch size, Hz, time)
    mel_sp_converted_norm = generatorM2F(mel_sp_norm)
    # (batch size, Hz, time) -> (Hz, time)
    mel_sp_converted_norm = mel_sp_converted_norm.squeeze(0)
    # torch -> numpy
    mel_sp_converted_norm = mel_sp_converted_norm.to('cpu').detach().numpy().copy()
    
    # numpy -> tensor
    mel_sp_converted = torch.from_numpy(mel_sp_converted.astype(np.float32)).clone()

    # mel sp -> wav
    # input  : tensor(batch size, Hz=80, time)
    # output : tensor(batch size, time)
    wav_transformed = hub_vocoder.inverse(mel_sp_converted) 
    wav_transformed = wav_transformed.squeeze(0) # wav_transformed (time)
    wav_transformed = wav_transformed.to('cpu').detach().numpy().copy() # tensor to numpy
    
    # librosa の output 関数はなかったので, wavファイルへの変換は soundfile モジュールを使用した
    sf.write(os.path.join(out_dir, os.path.basename(file_name)),
                                wav_transformed,
                                sampling_rate,
                                subtype="PCM_24")
