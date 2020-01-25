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
  var canvas = document.getElementById('ipmap');
  Post('/dynamic/iptrack', function(data) {
    if (data === null) {
      return;
    }
    var ctx = canvas.getContext('2d');
    var b = new Uint8Array(data);
    var img = ctx.createImageData(256, 256);
    var img_data = img.data;
    var pos = 0;
    var trail = 0;
    for (var i = 0; i < 256 * 32; i++) {
      for (var j = 0; j < 8; j++) {
        if (b[i] & (1 << j)) {
          trail = 20;
        }
        if (trail > 0) {
          --trail;
        }
        img_data[pos++] = Math.min(255, Math.floor(255 * trail / 10));
        img_data[pos++] = Math.floor(255 * trail / 20);
        img_data[pos++] = Math.floor(255 * trail / 30);
        img_data[pos++] = 255;
      }
    }
    ctx.putImageData(img, 0, 0);
  });
})();