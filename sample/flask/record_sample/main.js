main()

async function main () {
  const buttonStart = document.querySelector('#buttonStart')
  const buttonStop = document.querySelector('#buttonStop')
  const player = document.querySelector('#player')
  const downloadLink = document.getElementById('download');
  const recordedChunks = [];

  const stream = await navigator.mediaDevices.getUserMedia({ // <1>
    video: false,
    audio: true,
  })

  //audio/webmが対応しているかどうか
  if (!MediaRecorder.isTypeSupported('audio/webm')) { // <2>
    console.warn('audio/webm is not supported')
  }

  //mediaRecorderの作成
  const mediaRecorder = new MediaRecorder(stream, { // <3>
    mimeType: 'audio/webm',
  })

  //スタートボタンを押したときの処理
  buttonStart.addEventListener('click', () => {
    //録音スタート
    mediaRecorder.start() // <4>
    //スタートボタンをおせないように
    buttonStart.setAttribute('disabled', '')
    //ストップボタンを押せるように
    buttonStop.removeAttribute('disabled')
  })

  //ストップボタンを押したときの処理
  buttonStop.addEventListener('click', () => {
    //録音スタート
    mediaRecorder.stop() // <5>
    //スタートボタンをおせるように
    buttonStart.removeAttribute('disabled')
    //ストップボタンを押せ無いように
    buttonStop.setAttribute('disabled', '')
    //ファイルのダウンロード
    //Blobを使えばサーバー場に保存できそう？
    downloadLink.href = URL.createObjectURL(new Blob(recordedChunks));
    downloadLink.download = 'acetest.wav';
  })

  mediaRecorder.addEventListener('dataavailable', event => { // <6>
    player.src = URL.createObjectURL(event.data)
  })
}