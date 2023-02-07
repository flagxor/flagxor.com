'use strict';

(function() {

const SECRET = 'forth ';
var secretEntry = '';
var canvas, ctx;
var memory = new ArrayBuffer(16 * 1024 * 1024);
var u8 = new Uint8Array(memory);
var i32 = new Int32Array(memory);
var page = 0;

function Draw() {
  ctx.fillStyle = '#000';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.font = '20px consolas, courier';
  ctx.textBaseline = 'top';
  ctx.textAlign = 'left';
  var w = ctx.measureText('W').width;
  ctx.save();
  ctx.scale(canvas.width / (w * 64), canvas.height / (20 * 16));
  for (var j = 0; j < 15; ++j) {
    ctx.fillStyle = '#f70';
    ctx.fillText(j + ' : square dup * ;', 0, j * 20);
    ctx.fillStyle = '#fff';
    ctx.fillText(j + ' ( testing )', w * 32, j * 20);
  }
  ctx.fillStyle = '#07f';
  for (var j = 0; j < 64; ++j) {
    ctx.fillText(j % 10, j * w, 15 * 20);
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

  canvas = document.createElement('canvas');
  document.body.appendChild(canvas);
  window.addEventListener('resize', Resize);
  document.body.style.overflow = 'hidden';
  ctx = canvas.getContext('2d');
  Resize();
}

window.addEventListener('keydown', function(e) {
  if (secretEntry !== SECRET) {
    if (SECRET.startsWith(secretEntry + e.key)) {
      secretEntry += e.key;
    } else {
      secretEntry = '';
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
