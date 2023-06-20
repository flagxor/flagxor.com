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

0 value last-cache
1024 16 * constant chunk-size
4 constant cache-size
create cache-index cache-size cells allot
create cache-dirty cache-size cells allot
create cache-data cache-size chunk-size * allot

: index@ ( slot -- n ) cells cache-index + @ ;
: index! ( n slot -- ) cells cache-index + ! ;
: dirty@ ( slot -- n ) cells cache-dirty + @ ;
: dirty! ( n slot -- ) cells cache-dirty + ! ;
: chunk ( n -- a ) chunk-size * cache-data + ;

also forth definitions

: empty-buffers
  cache-size 0 do
    0 i dirty!
    -1 i index!
  loop
;
empty-buffers

: save-buffers
  cache-size 0 do
    i dirty@ i index@ 0< 0= and if
      i chunk i index@ server-write
      0 i dirty!
      -1 i index!
    then
  loop
;

: flush   save-buffers empty-buffers ;

: block ( n -- a )
  16 /mod { part n }
  n to last-cache
  cache-size 0 do
    i index@ n = if
      i chunk 1024 part * + unloop exit
    then
  loop
  cache-size 0 do
    i dirty@ 0= i index@ 0< or if
      i chunk n server-read
      n i index!
      i chunk 1024 part * +
      unloop exit
    then
  loop
  0 chunk 0 index@ server-write
  0 0 dirty!
  0 chunk n server-read
  n 0 index!
  0 chunk 1024 part * +
;

: buffer ( n -- a ) block ;
: update   -1 last-cache dirty! ;

only forth definitions

variable scr

( Loading )
: load ( n -- ) block 1024 evaluate ;
: thru ( a b -- ) over - 1+ for aft dup >r load r> 1+ then next drop ;

( Utility )
: copy ( from to -- )
   swap block pad 1024 cmove pad swap block 1024 cmove update ;

( Editing )
: list ( n -- ) scr ! ." Block " scr @ . cr scr @ block
   15 for dup 63 type [char] | emit space 15 r@ - . cr 64 + next drop ;
internals definitions
: clobber-line ( a -- a' ) dup 63 blank 63 + nl over c! 1+ ;
: @line ( n -- ) 64 * scr @ block + ;
: e' ( n -- ) @line clobber-line drop update ;
forth definitions internals
vocabulary editor   also editor definitions
: l    scr @ list ;   : n    1 scr +! l ;  : p   -1 scr +! l ;
: wipe   15 for r@ e' next l ;   : e   e' l ;
: d ( n -- ) dup 1+ @line swap @line 15 @line over - cmove 15 e ;
: r ( n "line" -- ) 0 parse 64 min rot dup e @line swap cmove l ;
: a ( n "line" -- ) dup @line over 1+ @line 16 @line over - cmove> r ;
only forth definitions
