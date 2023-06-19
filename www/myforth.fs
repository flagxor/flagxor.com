( Basic Demos )

web

JSWORD: pageload { a n -- }
  window.location.href = GetString(a, n);
~
: slides   s" https://flagxor.github.io/svfig-talks/svfig-2023-02-25/" pageload ;

( Special hooks )

web definitions

: passwd ( a n -- ) s" passwd" 0 setItem ;

JSWORD: raw-server-write { a n done -- }
  i32[done>>2] = -1;
  var request = new XMLHttpRequest();
  request.open('POST', '/dynamic/write');
  request.setRequestHeader('PASSWD', localStorage.getItem('passwd'));
  request.setRequestHeader('RECORD_NUMBER', n);
  request.onload = function() {
    if (request.status == 200) {
      i32[done>>2] = 0;
    } else {
      i32[done>>2] = 1;
    }
  };
  request.onerror = function() {
    i32[done>>2] = 2;
  };
  request.send(u8.slice(a, a + 1024 * 16));
~

JSWORD: raw-server-read { a n done -- }
  i32[done>>2] = -1;
  var request = new XMLHttpRequest();
  request.responseType = 'arraybuffer';
  request.open('POST', '/dynamic/read');
  request.setRequestHeader('PASSWD', localStorage.getItem('passwd'));
  request.setRequestHeader('RECORD_NUMBER', n);
  request.onload = function() {
    if (request.status == 200 &&
        request.response.byteLength == 1024 * 16) {
      var data = new Uint8Array(request.response);
      for (var i = 0; i < 1024 * 16; i++) {
        u8[a + i] = data[i];
      }
      i32[done>>2] = 0;
    } else {
      i32[done>>2] = 1;
    }
  };
  request.onerror = function() {
    i32[done>>2] = 2;
  };
  request.send();
~

also internals
: server-write ( a n -- )
   0 >r rp@ raw-server-write begin yield r@ 0< 0= until r@ throw rdrop ;
: server-read ( a n -- )
   0 >r rp@ raw-server-read begin yield r@ 0< 0= until r@ throw rdrop ;

only forth definitions
