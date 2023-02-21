'use strict';

var ueforth = null;

(function() {

const SECRET = 'forth';
var secretEntry = '';

function Init() {
  document.title = 'FORTH';
  var wrapper = document.getElementById('wrapper');
  wrapper.parentElement.removeChild(wrapper);

  var script = document.createElement('script');
  script.src = 'https://eforth.appspot.com/ueforth.js';
  document.body.appendChild(script);
  function Loader() {
    if (ueforth !== null) {
      ueforth.Start();
    } else {
      setTimeout(Loader, 10);
    }
  }
  Loader();
  window.removeEventListener('keydown', Intercept);
}

function Intercept(e) {
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
}

window.addEventListener('keydown', Intercept);

})();
