'use strict';

(function() {

const SECRET = 'forth';
var secretEntry = '';

function Init() {
  var wrapper = document.getElementById('wrapper');
  wrapper.parentElement.removeChild(wrapper);
  document.title = 'FORTH';
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
  }
});

window.addEventListener('keyup', function(e) {
});

})();
