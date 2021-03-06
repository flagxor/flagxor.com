needs posix.fs
needs scgi.fs

get-current vocabulary iptrack also iptrack definitions ( private )

256 256 * 8 / constant data-size
s" iptrack.data$" sz O_RDWR O_CREAT or octal 660 decimal open
  constant state-file
state-file 0< throw ( check that it opens )
state-file data-size ftruncate throw
0 data-size PROT_READ PROT_WRITE or
  MAP_SHARED state-file 0 mmap constant data
: save data data-size MS_ASYNC msync drop ; save

: byte-clip ( n -- n ) 0 max 255 min ;
: 1trim ( a n -- a n ) 1- 0 max swap 1+ swap ;
: ip-parts ( -- a b )
  0 0 s" REMOTE_ADDR" param >number
  1trim 0 -rot 0 -rot >number 2drop
  drop swap drop
  byte-clip swap byte-clip swap
;

: or! ( n a -- ) dup -rot c@ or swap c! ;
: bitmap-pos ( x y -- m a ) 32 * swap 8 /mod swap 1 swap lshift -rot + data + ;
: mark-ip ip-parts bitmap-pos or! save ;

: respond-iptrack
  ok-octet
  mark-ip
  data data-size rtype
;

set-current ( public )

: respond-iptrack respond-iptrack ;

previous
