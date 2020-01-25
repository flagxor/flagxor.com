needs posix.fs
needs scgi.fs
needs synch.fs

get-current vocabulary boardtoy also boardtoy definitions ( private )

64 constant board-size
4096 constant data-size
s" boardtoy.data$" sz O_RDWR O_CREAT or octal 660 decimal open
  constant state-file
state-file 0< throw ( check that it opens )
state-file data-size ftruncate throw
0 data-size PROT_READ PROT_WRITE or
  MAP_SHARED state-file 0 mmap constant data
: save data data-size MS_ASYNC msync drop ; save

: stall ( n -- ) 2/ data l@ dup 0= if drop 1 then = if await then ;

: advance   data l@ 1+ data l! ;

: interact ( n -- )
  2/ dup 255 and swap 8 rshift 255 and data + c!
  advance save awake
;

: handle-input
  0 0 s" QUERY_STRING" param >number 2drop drop
  dup 1 and if interact else stall then
;

: respond-boardtoy
  handle-input
  ok-octet
  data board-size rtype
;

set-current ( public )

: respond-boardtoy respond-boardtoy ;

previous
