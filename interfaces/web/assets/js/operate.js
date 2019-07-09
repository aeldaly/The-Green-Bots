
(function ($) {
    $(document).ready(function () {
        'use strict'

        var serverURL = "http://thegreenbot.local";
        // var serverURL = "http://localhost:8000";
        const cameraURL = serverURL + "/api/operate/camera";
        const controlURL = serverURL + "/api/operate/control";

        var imageObj = new Image();
        imageObj.onload = function () {
            drawOnCanvas();
            setTimeout(timedRefresh, 10);
        }
        // set src AFTER assigning load
        $.get(cameraURL, function(data, status){
            imageObj.src = "data:image/png;base64," + data;
        });

        function timedRefresh() {
            $.get(cameraURL, function(data, status){
                imageObj.src = "data:image/png;base64," + data;
            });
        }

        function drawOnCanvas() {
            var canvas = document.getElementById("canvas");
            var ctx = canvas.getContext("2d");
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(imageObj, 0, 0, canvas.width, canvas.height);
        }

        document.onkeydown = checkKey;

        function checkKey(e) {
            var controlKey = null;
            e = e || window.event;
            if (e.keyCode == '38') {
                // up arrow
                console.log('up arrow')
                document.getElementById('control').value = 'Up';
                controlKey = 'up';
            }
            else if (e.keyCode == '40') {
                // down arrow
                console.log('down arrow')
                document.getElementById('control').value = 'Down';
                controlKey = 'down';
            }
            else if (e.keyCode == '37') {
            // left arrow
                console.log('left arrow')
                document.getElementById('control').value = 'Left';
                controlKey = 'left';
            }
            else if (e.keyCode == '39') {
            // right arrow
                console.log('right arrow')
                document.getElementById('control').value = 'Right';
                controlKey = 'right';
            }
            if (controlKey != null){
                $.ajax({
                    url: controlURL,
                    type: 'post',
                    dataType: 'json',
                    data: JSON.stringify(controlKey),
                    success: function(data) {
                      console.log('Control key sent to backend...')
                    }
                });
            }
        }

    });
})($);