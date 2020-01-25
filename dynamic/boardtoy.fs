needs posix.fs
needs scgi.fs

get-current vocabulary boardtoy also boardtoy definitions ( private )

4096 constant data-size
s" boardtoy.data$" sz O_RDWR O_CREAT or octal 660 decimal open
  constant state-file
state-file 0< throw ( check that it opens )
state-file data-size ftruncate throw
0 data-size PROT_READ PROT_WRITE or
  MAP_SHARED state-file 0 mmap constant data
: save data data-size MS_ASYNC msync drop ; save

: respond-boardtoy
  0 0 s" QUERY_STRING" param >number 2drop nip
  ok-text
  0 <# #s #> rtype
;

set-current ( public )

: respond-boardtoy respond-boardtoy ;

previous
