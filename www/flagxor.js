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
    var ctx = canvas_hidden.getContext('2d');
    var b = new Uint8Array(data);
    var img = ctx.createImageData(256, 256);
    var img_data = img.data;
    var pos = 0;
    function sample(x, y) {
      if (x < 0 || x >= 256 || y < 0 || y >= 256) {
        return 0;
      }
      var i = y * 32 + (x >> 3);
      var j = x & 7;
      return (b[i] & (1 << j)) != 0;
    }
    for (var i = 0; i < 256; i++) {
      for (var j = 0; j < 256; j++) {
        var a = 0;
        var b = 0;
        for (var x = -10; x <= 10; x++) {
          for (var y = -10; y <= 10; y++) {
            if (sample(i + x, j + y)) {
              if (x * x + y * y < 10 * 10) {
                a++;
              }
              if (x * x + y * y < 3 * 3) {
                b++;
              }
            }
          }
        }
        a = Math.floor(a * 255 / (21 * 21));
        b = Math.floor(b * 255 / (7 * 7));
        img_data[pos++] = Math.min(a, b);
        img_data[pos++] = Math.min(a / 2, b);
        img_data[pos++] = b;
        img_data[pos++] = 255;
      }
    }
    ctx.putImageData(img, 0, 0);
  });
})();
