var startButton = document.getElementById("start");
var stopButton = document.getElementById("stop");
var mediaRecorder;
var localStream;

startButton.onclick = function () {
    navigator.mediaDevices.getUserMedia({audio: true })
        .then(function (stream) {
            localStream = stream;
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();
            console.log("Status: " + mediaRecorder.state);
        }).catch(function (err) {
            console.log(err);
        });
}
stopButton.onclick = function () {
    mediaRecorder.stop();
    console.log("Status: " + mediaRecorder.state);
    mediaRecorder.ondataavailable = function (event) {
        document.getElementById("audio").src = window.URL.createObjectURL(event.data);
    }
    localStream.getTracks().forEach(track => track.stop());
}