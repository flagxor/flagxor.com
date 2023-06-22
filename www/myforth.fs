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
  request.open('POST', '/dynamic/write?' + n);
  request.setRequestHeader('PASSWD', localStorage.getItem('passwd'));
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
  request.open('POST', '/dynamic/read?' + n);
  request.setRequestHeader('PASSWD', localStorage.getItem('passwd'));
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

variable available
variable dirty
variable resident

0 value last-cache
1024 16 * constant chunk-size
4 constant cache-size

: >index ( a -- a ) cell + ;
: >data ( a -- a ) 2 cells + ;

: add-first { a dst -- } dst @ a ! a dst ! ;
: take-first { src -- a } src @ src @ @ src ! ;
: take-last { src -- a }
  src begin dup @ @ while @ repeat dup @ swap 0 swap ! ;

: add-cache   here 0 , 0 , chunk-size allot available add-first ;
: init-cache   cache-size 0 do add-cache loop ; init-cache

: pluck { n src -- a }
  src begin dup @ while
    dup @ >index @ n = if
      dup @ >r dup @ @ swap ! r> exit
    then
    @
  repeat @
;

: front-it { n src -- a } n src pluck dup if dup src add-first then ;

: read-it ( a -- ) dup >data swap >index @ server-read ;
: write-it ( a -- ) dup >data swap >index @ server-write ;

: count-it { src -- n }
  0 { tally }
  src begin dup @ while 1 +to tally @ repeat drop tally ;

also forth definitions

: empty-buffers
  begin resident @ while resident take-first available add-first repeat
  begin dirty @ while dirty take-first available add-first repeat
;

: save-buffers
  begin dirty @ while
    dirty take-first
    dup write-it
    resident add-first
  repeat
;

: flush   save-buffers empty-buffers ;

: free-block ( -- a )
  available @ if available take-first resident add-first resident @ exit then
  resident @ if resident take-last exit then
  dirty @ 0= throw
  dirty take-last
  dup write-it
  available add-first
;

: block ( n -- a )
  16 /mod { part n } n to last-cache
  n dirty front-it if dirty @ >data part 1024 * + exit then
  n resident front-it if resident @ >data part 1024 * + exit then
  free-block
  n over >index !
  dup read-it
  >data part 1024 * +
;

: buffer ( n -- a ) block ;

: update
  resident @ 0= if exit then
  resident @ >index @ last-cache = if
    resident take-first dirty add-first
  then
;

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
