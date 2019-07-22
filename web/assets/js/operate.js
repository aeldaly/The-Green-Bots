var controlSignal;
$(document).ready(function() {
    'use strict'

    var serverURL = "http://thegreenbot.local";
    // var serverURL = "http://localhost:8000";
    const cameraURL = serverURL + "/api/operate/camera";
    const controlURL = serverURL + "/api/operate/control";

    const refreshInterval = 1;

    function timedRefresh() {
        $.ajax({
            url: cameraURL + "?t=" + new Date().getTime(),
            type: 'get',
            cache: false,
            success: function(data){
                imageObj.src = "data:image/png;base64," + data;
            },
            error: function(){
                console.log('error!');
                setTimeout(timedRefresh, refreshInterval);
            }
        });
    }
    function drawOnCanvas() {
        var canvas = document.getElementById("canvas");
        var ctx = canvas.getContext("2d");
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(imageObj, 0, 0, canvas.width, canvas.height);
    }

    var imageObj = new Image();
    imageObj.onload = function () {
        drawOnCanvas();
        setTimeout(timedRefresh, refreshInterval);
    }

    timedRefresh();

    function sendControlData(controlKey) {
        $.ajax({
            url: controlURL,
            type: 'post',
            dataType: 'json',
            data: JSON.stringify(controlKey),
            success: function(data) {
                document.getElementById('control').value = controlKey;
                console.log('Control key sent to backend...')
            }
        });
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
        if (controlKey != null){
            sendControlData(controlKey);
        }
    }
    controlSignal = function (key) {
        console.log(key)
        sendControlData(key);
    }
});
