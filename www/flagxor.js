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
  Post('/dynamic/iptrack', function(data) {
    if (data === null) {
      return;
    }
    var ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, w, h);
    var b = new Uint8Array(data.buffer);
    var img = ctx.createImageData(256, 256);
    var img_data = img.data;
    var pos = 0;
    for (var i = 0; i < 256 * 32; i++) {
      for (var j = 0; j < 8; j++) {
        img_data[pos++] = (b[i] & (1 << j)) ? 255 : 0;
        img_data[pos++] = 0;
        img_data[pos++] = 0;
        img_data[pos++] = 255;
      }
    }
    ctx.putImage(img, 0, 0);
  });
})();
