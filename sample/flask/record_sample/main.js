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

  if (!MediaRecorder.isTypeSupported('audio/webm')) { // <2>
    console.warn('audio/webm is not supported')
  }
  const mediaRecorder = new MediaRecorder(stream, { // <3>
    mimeType: 'audio/webm',
  })

  mediaRecorder.addEventListener('dataavailable', function(e) {
    if (e.data.size > 0) recordedChunks.push(e.data);
  });


  buttonStart.addEventListener('click', () => {
    mediaRecorder.start() // <4>
    buttonStart.setAttribute('disabled', '')
    buttonStop.removeAttribute('disabled')
  })

  buttonStop.addEventListener('click', () => {
    mediaRecorder.stop() // <5>
    buttonStart.removeAttribute('disabled')
    buttonStop.setAttribute('disabled', '')
    downloadLink.href = URL.createObjectURL(new Blob(recordedChunks));
    downloadLink.download = 'acetest.wav';
  })

  mediaRecorder.addEventListener('dataavailable', event => { // <6>
    player.src = URL.createObjectURL(event.data)
  })
}