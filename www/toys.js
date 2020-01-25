'use strict';

(function() {

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

function IpMap() {
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
}

var board_state;

function Draw() {
  var canvas = document.getElementById('board');
  var ctx = canvas.getContext('2d');
  ctx.fillStyle = '#000';
  ctx.fillRect(0, 0, 256, 256);
  ctx.fillStyle = '#ff0';
  ctx.font = '20px Helvetica, Arial, san-serif';
  ctx.fillText(board_state[4], board_state[5], 'Forth');
}

function Move(x, y) {
  x = Math.max(0, Math.min(255, x | 0));
  y = Math.max(0, Math.min(255, y | 0));
  Post('/dynamic/boardtoy?' + ((0 * 256 + x) * 2 + 1), function(data) {});
  Post('/dynamic/boardtoy?' + ((1 * 256 + y) * 2 + 1), function(data) {});
}

function Board() {
  var code = 0;
  if (board_state) {
    var d = new Uint32Array(board_state);
    code = d[0];
  }
  Post('/dynamic/boardtoy?' + (code * 2), function(data) {
    if (data === null) {
      return;
    }
    board_state = new Uint8Array(data);
    Draw();
    Board();
  });
}

function Main() {
  IpMap();
  Board();
  var canvas = document.getElementById('board');
  canvas.onmousedown = function(e) {
    Move(e.clientX, e.clientY);
  };
}

Main();

})();
