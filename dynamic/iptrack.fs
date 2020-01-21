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

: respond-iptrack
  ok-text
  s" REMOTE_ADDR" param rtypeln 
;

set-current ( public )

: respond-iptrack respond-iptrack ;

previous
