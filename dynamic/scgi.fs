#! /usr/bin/env gforth

needs posix.fs

get-current vocabulary scgi also scgi definitions ( private )

5 constant workers

( Check for stack leaks )
: ground depth throw ;
( Parsing utils )
: drop-trailing   source nip >in ! ;
: eat-trailing ( -- a n ) source >in @ - swap >in @ + swap drop-trailing ;

65536 constant inbuf-max  100 constant inbuf-padding
inbuf-max inbuf-padding + constant inbuf-total
create inbuf inbuf-total allot
variable inbuf#
variable request
: inbuf-clear inbuf inbuf-total 0 fill ;

variable goal
variable goal#
: end< ( n -- f ) inbuf# @ < ;
: in@<> ( n ch -- f ) >r inbuf + c@ r> <> ;
: first0 0 begin dup [char] : in@<> over end< and while 1+ repeat 1+ ;
: skipto0 begin dup 0 in@<> over end< and while 1+ repeat ;
: next0 dup inbuf + swap skipto0 dup 1+ -rot inbuf + over - ;
: param
  goal# ! goal ! first0
  begin dup end< while
    next0 goal @ goal# @ str= if next0 rot drop exit then
    next0 2drop
  repeat drop s" "
;

create crlf_ 13 c, 10 c, does> 2 ;
: rtype request @ -rot write drop ;
: rcr crlf_ rtype ;
: rtypeln rtype rcr ;

variable handler  variable incoming
: close-request request @ close drop ;
: read-request inbuf-clear request @ inbuf inbuf-max read inbuf# ! ;
: handle-request read-request handler @ execute close-request ;
: handle-one incoming @ sockaccept request ! handle-request ;
: handle-all begin handle-one ground again ;
: setup ( handler port -- )
   bind incoming !
   handler !
   incoming @ workers 2* listen throw
;
variable retcode
: run ( handler port -- )
   setup workers 0 do fork 0= if handle-all unloop exit then loop
   workers 0 do -1 retcode 0 waitpid drop ground loop bye ;

set-current ( public )

: param param ;
: rtype rtype ;
: rtypeln rtypeln ;
: rcr rcr ;
: scgi-run ( handler port -- ) run ;

: notfound s" Status: 404 Not Found" rtypeln rcr ;
: status-ok s" Status: 200 OK" rtypeln ;
: plain-text s" Content-Type: text/plain" rtypeln ;
: html-text s" Content-Type: text/html" rtypeln ;
: octet-stream s" Content-Type: application/octet-stream" rtypeln ;
: ok-text status-ok plain-text rcr ;
: ok-html status-ok html-text rcr ;
: ok-octet status-ok octet-stream rcr ;

: r\ eat-trailing postpone sliteral postpone rtypeln ; immediate

previous
