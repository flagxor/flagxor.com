'use strict';

(function() {

const SECRET = 'forth';
var secretEntry = '';
var canvas, ctx;

function Draw() {
  ctx.fillStyle = '#000';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = '#ff0';
  ctx.fillRect(0, 0, canvas.width / 2, canvas.height / 2);
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
  e.preventDefault();
});

window.addEventListener('keyup', function(e) {
  e.preventDefault();
});

})();
