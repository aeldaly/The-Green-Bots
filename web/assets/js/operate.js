var img = document.getElementById("liveImg");
var fpsText = document.getElementById("fps");

var target_fps = 24;

var request_start_time = performance.now();
var start_time = performance.now();
var time = 0;
var request_time = 0;
var time_smoothing = 0.9; // larger=more smoothing
var request_time_smoothing = 0.2; // larger=more smoothing
var target_time = 1000 / target_fps;

var wsCamera;
var wsDrive;

function requestImage() {
    request_start_time = performance.now();
    wsCamera.send(1);
}


$(document).ready(function() {
    'use strict'

    var serverURL = "http://thegreenbot.local";
    // var serverURL = "http://localhost:8000";
    const cameraURL = serverURL + "/api/operate/camera";
    const controlURL = serverURL + "/api/operate/control";

    if ("WebSocket" in window) {
        var wsProtocol = (location.protocol === "https:") ? "wss://" : "ws://";
        // Camera

        wsCamera = new WebSocket(wsProtocol + "thegreenbot.local" + "/api/operate/camera");
        wsCamera.binaryType = 'arraybuffer';

        wsCamera.onopen = function() {
            console.log("connection was established");
            start_time = performance.now();
            requestImage();
        };
        
        wsCamera.onmessage = function(evt) {
            var arrayBuffer = evt.data;
            var blob  = new Blob([new Uint8Array(arrayBuffer)], {type: "image/jpeg"});
            img.src = window.URL.createObjectURL(blob);
            var end_time = performance.now();
            var current_time = end_time - start_time;
            // smooth with moving average
            time = (time * time_smoothing) + (current_time * (1.0 - time_smoothing));
            start_time = end_time;
            var fps = Math.round(1000 / time);
            fpsText.textContent = fps;
        
            var current_request_time = performance.now() - request_start_time;
            // smooth with moving average
            request_time = (request_time * request_time_smoothing) + (current_request_time * (1.0 - request_time_smoothing));
            var timeout = Math.max(0, target_time - request_time);
        
            setTimeout(requestImage, timeout);
        };

        wsCamera.onerror = function (e) {
            console.log(e);
            wsCamera.send(1);
        };

        // Drive

        wsDrive = new WebSocket(wsProtocol + "thegreenbot.local" + "/api/operate/drive");
        // ws.binaryType = 'arraybuffer';

        wsDrive.onopen = function() {
            console.log("connection was established for Drive");
        };
        
        wsDrive.onmessage = function(evt) {
            var message = evt.data;
            document.getElementById('control').value = message;
        };

        wsDrive.onerror = function (e) {
            console.log(e);
            wsDrive.send('stop');
        };

    } else {
        alert("WebSocket not supported");
    }

    function sendControlData(controlKey) {
        wsDrive.send(controlKey)
    }

    document.onkeydown = checkKey;

    function checkKey(e) {
        var controlKey = null;
        e = e || window.event;
        if (e.keyCode == '38') {
            // up arrow
            console.log('forward arrow')
            controlKey = 'forward';
        }
        else if (e.keyCode == '40') {
            // down arrow
            console.log('reverse arrow')
            controlKey = 'reverse';
        }
        else if (e.keyCode == '37') {
        // left arrow
            console.log('left arrow')
            controlKey = 'left';
        }
        else if (e.keyCode == '39') {
        // right arrow
            console.log('right arrow')
            controlKey = 'right';
        }
        else if (e.keyCode == '32') {
        // space bar
            console.log('stop - space bar')
            controlKey = 'stop';
        }
        if (controlKey != null){
            sendControlData(controlKey);
        }
    }

    // window.addEventListener('resize', resizeCanvas, false);
    // resizeCanvas();    /// call the first time page is loaded
    // function resizeCanvas() {
    //     canvas.width = window.innerWidth;
    //     canvas.height = window.innerHeight;
    // }
});
