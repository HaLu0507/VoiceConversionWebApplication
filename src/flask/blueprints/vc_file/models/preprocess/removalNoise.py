from scipy.io import wavfile
import numpy as np
import librosa
import soundfile as sf

#乱数の種を設定
np.random.seed(0)

def stft(x, sr, frame_shift=0, n_fft=2048):
    """短時間フーリエ変換を行うメソッド
    
    Args:
        x : 1次元の音声配列
        sr (int): 音声のサンプリング周波数
        frame_shift (int): 音声を切り取る長さ
        n_fft (int): 窓幅 (0以外の値を持つ区間の長さ)
        
    Returns:
        X : スペクトログラム
    """
    if frame_shift == 0:
        frame_shift=int(sr * 0.005)
        
    # STFT
    X = librosa.stft(x.astype(np.float32), n_fft=n_fft, win_length=n_fft, hop_length=frame_shift, window="hann")
    
    return X

def istft(X, sr, frame_shift=0, n_fft=2048):
    """逆フーリエ変換を行うメソッド
    
    Args: 
        X : スペクトルグラム, 
            shape=(A,B)のとき, A:周波数成分, B:シフトした回数(時間成分)
        
        sr : 音声の周波数
        frame_shift : 音声を移動する長さ
        n_fft : 窓幅 (0以外の値を持つ区間の長さ)
    """
    if frame_shift == 0:
        frame_shift = int(sr * 0.005)
    
    # ISTFT
    x_hat = librosa.istft(X, win_length=n_fft, hop_length=frame_shift, window="hann")
    
    return x_hat

def wienerFilter(x, sr, begin_t=0, end_t=0, mu=1.0, alpha=2.0, e_per=0.01):
    """
    ウィナーフィルタによる背景雑音の除去を行うメソッド
    ※ 雑音だけが存在する時間がある場合に有効

    x  : 1次元の音声配列
    sr : 周波数

    begin_t : 雑音だけが始まる時刻
    end_t   : 雑音だけが終わる時刻

    スペクトルサブトラクションのパラメータ
    mu, alpha : 大きい値に設定することで, 雑音を強く抑制する.
    e_per     : 振幅の何％下回らないようにするか
    """

    #乱数の種を設定
    np.random.seed(0)
    
    # フーリエ変換
    stft_data = stft(x,sr)

    #入力信号の振幅を取得
    amp=np.abs(stft_data)

    #入力信号のパワーを取得
    input_power=np.power(amp,2.0)
    
    #雑音だけが始まる時刻
    begin_n_noise_only_index=int(begin_t*sr)
    #雑音だけが終わる時刻
    end_n_noise_only_index=int(end_t*sr)

    #雑音のパワーを推定
    noise_power=np.mean(np.power(amp,2.0)[:,begin_n_noise_only_index:end_n_noise_only_index],axis=1,keepdims=True)

    #入力信号の音量の1%を下回らないようにする
    eps=e_per*input_power

    #出力信号の振幅を計算する
    processed_power=np.maximum(input_power-alpha*noise_power,eps)

    #比率
    wf_ratio= processed_power/(processed_power+mu*noise_power)

    #出力信号の振幅に入力信号の位相をかける
    processed_stft_data=wf_ratio*stft_data

    #時間領域の波形に戻す
    removalNoiseData = istft(processed_stft_data, sr)
    
    return removalNoiseData
    
def removalBackgroundNoise(file_path):
    """ 背景ノイズを削除するメソッド

    Args:
        file_path : 対象となる音声データのパス
    """
    
    # データをロード
    sr, x = wavfile.read(file_path)

    # ウィナーフィルタによる背景雑音の削除
    # 雑音時間は 0 ~ 0.05s と設定している
    removalNoiseData = wienerFilter(x=x, sr=sr, begin_t=0, end_t=0.05)

    # データを保存する
    removalNoiseData = removalNoiseData / max(abs(removalNoiseData))
    wavfile.write(filename=file_path, rate=sr, data=removalNoiseData)