$(document).ready(function() {
    var image = new Array()
    var video = document.getElementById('video');
    // var data   = new FormData();


    // Get access to the camera!
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        // Not adding `{ audio: true }` since we only want video now
        navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
            //video.src = window.URL.createObjectURL(stream);
            video.srcObject = stream;
            video.play();
        });
    }

    var canvas = document.getElementById('canvas-sf');
    var context = canvas.getContext('2d');
    var video = document.getElementById('video');



    function dpImage(show) {

        if (show === true) {
            $('#canvas-sf').show()
            $('#image-sf').hide()
        } else {
            $('#image-sf').show()
            $('#canvas-sf').hide()
        }

    }


    $('#load-im1').change(function() {
        if (this.files && this.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
                $('#image-sf')
                    .attr('src', e.target.result)
                    .width(400)


            };
            image[0] = this.files[0]
            reader.readAsDataURL(this.files[0]);
        }
        dpImage(false)
    })


    $('#submit').click(function() {
        var data   = new FormData();
        image.forEach(function(im, i) {
            data.append('image_' + i, im);
        });
        $.ajax({
            type: "post",
            processData: false,
            contentType: false,
            data: data,
            url: "http://localhost:3000/upload/images",
            success: function(res) {
                console.log(res)
                $('#icon-loading').hide()
                var html = ''
                html += '<h2>' + res + '</h2>'
                document.getElementById('verify').innerHTML = html
                $('#verify').show();
            },
            error: function() {
                $('#icon-loading').hide()
            },
        })

    })

})