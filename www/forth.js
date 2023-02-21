'use strict';

(function() {

const SECRET = 'forth ';
var secretEntry = '';

var canvas, ctx;

var memory = new ArrayBuffer(16 * 1024 * 1024);
var u8 = new Uint8Array(memory);
var i32 = new Int32Array(memory);
var page = 0;

var COLORS = {
  0: '#fff',
  1: '#f00',
  2: '#f70',
  3: '#ff0',
  4: '#7f0',
  5: '#0f0',
  6: '#0f7',
  7: '#0ff',
  8: '#07f',
  9: '#00f',
  10: '#70f',
  11: '#f0f',
  12: '#f07',
};

function Draw() {
  ctx.fillStyle = '#000';
  ctx.font = '20px consolas, courier';
  ctx.textBaseline = 'top';
  ctx.textAlign = 'left';
  var w = ctx.measureText('W').width;
  ctx.save();
  ctx.scale(canvas.width / (w * 64), canvas.height / (20 * 16));
  var color = '#fff';
  for (var pos = 1023; pos >= 0; --pos) {
    var i = pos % 64;
    var j = Math.floor(pos / 64);
    var ch = u8[pos];
    if (COLORS[ch & 0x7f] !== undefined) {
      color = COLORS[ch & 0x7f];
      ch = (ch & 0x80) | 32;
    }
    if ((ch & 0x7f) < 32 || (ch & 0x7f) == 127) {
      ch = (ch & 0x80) | 32;
    }
    if (ch > 128) {
      var fg = '#000';
      var bg = color;
    } else {
      var bg = '#000';
      var fg = color;
    }
    ctx.fillStyle = bg;
    ctx.fillRect(i * w, j * 20, w, 20);
    ctx.fillStyle = fg;
    ctx.fillText(String.fromCharCode(ch & 0x7f), i * w, j * 20);
  }
  ctx.restore();
}

function Resize() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  Draw();
}

function Init() {
  document.title = 'FORTH';
  var wrapper = document.getElementById('wrapper');
  wrapper.parentElement.removeChild(wrapper);

  for (var i = 0; i < 1024; ++i) {
    u8[i] = Math.floor(Math.random() * 256);
  }

  canvas = document.createElement('canvas');
  document.body.appendChild(canvas);
  window.addEventListener('resize', Resize);
  document.body.style.overflow = 'hidden';
  ctx = canvas.getContext('2d');
  Resize();
}

window.addEventListener('keydown', function(e) {
  if (secretEntry !== SECRET) {
    secretEntry += e.key;
    while (secretEntry.length > SECRET.length) {
      secretEntry = secretEntry.substr(1);
    }
    if (secretEntry === SECRET) {
      Init();
    }
    return;
  }
//  e.preventDefault();
});

window.addEventListener('keyup', function(e) {
//  e.preventDefault();
});

})();
