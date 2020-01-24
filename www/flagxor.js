'use strict';

function Post(url, callback) {
  var r = new XMLHttpRequest();
  r.responseType = 'arraybuffer';
  r.addEventListener('readystatechange', function() {
    if (r.readyState === XMLHttpRequest.DONE) {
      if (r.status === 200) {
        callback(r.response);
      } else {
        callback(null);
      }
    }
  });
  r.open('POST', url);
  r.send();
}

(function() {
  var canvas = document.getElementById('iptrack');
  var canvas_hidden = document.getElementById('iptrack_hidden');
  Post('/dynamic/iptrack', function(data) {
    if (data === null) {
      return;
    }
    var ctx = canvas_hidden.getContext('2d');
    var b = new Uint8Array(data);
    var img = ctx.createImageData(256, 256);
    var img_data = img.data;
    var pos = 0;
    for (var i = 0; i < 256 * 32; i++) {
      for (var j = 0; j < 8; j++) {
        if (b[i] & (1 << j)) {
          img_data[pos++] = 255;
          img_data[pos++] = 192;
          img_data[pos++] = 0;
          img_data[pos++] = 0;
        } else {
          img_data[pos++] = 0;
          img_data[pos++] = 0;
          img_data[pos++] = 0;
          img_data[pos++] = 0;
        }
      }
    }
    ctx.putImageData(img, 0, 0);

    var ctx = canvas.getContext('2d');
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, 256, 256);
    ctx.filter = 'blur(10px);';
    ctx.drawImage(canvas_hidden, 0, 0);
    ctx.filter = 'grayscale(); blur(2px);';
    ctx.drawImage(canvas_hidden, 0, 0);
    ctx.filter = '';
  });
})();
