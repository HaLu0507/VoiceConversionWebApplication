# このファイルを直接実行する場合
# from Generator import Generator
# import preprocess

# このファイルを直接実行しない場合
from .Generator import Generator
from . import preprocess

import torch
import librosa 
import numpy as np
import soundfile as sf
import argparse

# melGAN
vocoder = torch.hub.load('descriptinc/melgan-neurips', 'load_melgan', model_name='multi_speaker')

def normalize_mel(wav):
    """ 音声をメルスペクトログラムに変換し, 正規化するメソッド

    Args:
        wav numpy(Time,) : 音声データ
    
    Return:
        mel_normalized torch(1, Hz, Time) : 正規化されたメルスペクトログラム
    """

    # wav -> mel-spec
    spec = vocoder(torch.tensor([wav]))
    # print(f"spec shape : {spec.shape}") # maybe (1, Hz, Time)
    # tensor -> numpy
    spec = spec.cpu().detach().numpy()[0] # spec shape : (Hz, Time)

    # get mean & std
    mel_mean = np.mean(spec, axis=1, keepdims=True)
    mel_std = np.std(spec, axis=1, keepdims=True) + 1e-9
    # normalize mel-spec
    mel_normalized = (spec - mel_mean) / mel_std

    # numpy -> tensor
    mel_normalized = torch.from_numpy(mel_normalized).float()
    # shape(Hz, Time) -> shape(1, Hz, Time)
    mel_normalized = mel_normalized.unsqueeze(0)

    return mel_normalized
    
def convert(file_name, file_path, mode):
    """ 引数で与えられた音声ファイルを変換し, 変換した音声ファイルを保存するメソッド
        convert()メソッドと異なり正規化を行なっている.

    Args:
        file_name : 音声のファイル名
        file_path : 変換前の音声のパス
        mode : convertM2W if male -> female else convertW2M
    """

    # 変換した音声を保存するディレクトリ
    # app.py から見た時の相対パスになっている
    out_dir = "./music/converted_" 

    # モデルの生成
    generatorF2M = Generator().to('cpu')
    generatorM2F = Generator().to('cpu')

    # モデルのチェックポイントをロードする
    checkPoint = torch.load("./models/converters/CycleGAN_VC2/_CycleGAN_CheckPoint", torch.device('cpu'))
    generatorF2M.load_state_dict(
        state_dict=checkPoint['model_genA2B_state_dict'])
    generatorM2F.load_state_dict(
        state_dict=checkPoint['model_genB2A_state_dict'])
    
    # Speech Parameters
    mel_sps_normalization = np.load("./models/converters/CycleGAN_VC2/norm_stats/mel_sps_normalization.npz")
    female_mel_mean = mel_sps_normalization['mean_A']
    female_mel_std = mel_sps_normalization['std_A']
    male_mel_mean = mel_sps_normalization['mean_B']
    male_mel_std = mel_sps_normalization['std_B']
    
    # 前処理
    # hyper parameters
    n_mel_channels = 80
    sampling_rate = 22050 # default : 16000
    frame_period = 5.0

    # 音声データの読み込み
    wav, _ = librosa.load(file_path, sr=sampling_rate, mono=True)
    wav = preprocess.wav_padding(wav=wav,
                                    sr=sampling_rate,
                                    frame_period=frame_period,
                                    multiple=4)
    
    # 正規化されたメルスペクトログラムを取得
    mel_normalized = normalize_mel(wav)

    # conversion
    # converted_mel_normalized : torch(1, Hz, Time)
    if mode == "convertM2F": # convert male 2 female
        converted_mel_normalized = generatorM2F(mel_normalized)
    else: # convert female 2 male
        converted_mel_normalized = generatorF2M(mel_normalized)


    # torch -> numpy & mel_normalized -> mel & numpy -> torch
    converted_mel_normalized = converted_mel_normalized.to('cpu').detach().numpy().copy()
    if mode == "convertM2F": # male 2 female
        converted_mel = (converted_mel_normalized * female_mel_std) + female_mel_mean
    else: # female 2 male
        converted_mel = (converted_mel_normalized * male_mel_std) + male_mel_mean
    converted_mel = torch.from_numpy(converted_mel.astype(np.float32)).clone()

    # mel sp -> wav
    # input  : tensor(batch size, Hz=80, time)
    # output : tensor(batch size, time)
    wav_transformed = vocoder.inverse(converted_mel) 
    wav_transformed = wav_transformed.squeeze(0) # wav_transformed (time)
    wav_transformed = wav_transformed.to('cpu').detach().numpy().copy() # tensor to numpy
    
    # librosa の output 関数はなかったので, wavファイルへの変換は soundfile モジュールを使用した
    sf.write(f"{out_dir}{file_name}",
             wav_transformed,
             sampling_rate,
             subtype="PCM_24")

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Conversion settings")
    
    parser.add_argument('--file_name', type=str, help="wav file name")
    parser.add_argument('--file_path', type=str, help="wav file path")
    parser.add_argument('--mode', type=str, help="which conversion male to female or female to male")

    argv = parser.parse_args()
    
    convert(argv.file_name, argv.file_path, argv.mode)
