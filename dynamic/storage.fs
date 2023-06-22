needs posix.fs
needs scgi.fs
needs synch.fs

get-current vocabulary storage also scgi also storage definitions ( private )

s" passwd" r/o open-file throw constant passwd-file
100 constant max-passwd
create passwd max-passwd allot
passwd max-passwd passwd-file read-file throw 1- constant passwd#
passwd-file close-file throw

1024 16 * constant block-size
128 constant public-block-count
1024 constant block-count
block-size block-count * constant data-size
s" storage.data$" sz O_RDWR O_CREAT or octal 660 decimal open
  constant state-file
state-file 0< throw ( check that it opens )
state-file data-size ftruncate throw
0 data-size PROT_READ PROT_WRITE or
  MAP_SHARED state-file 0 mmap constant data
: save data data-size MS_ASYNC msync drop ; save
: data-block ( n -- a ) block-size * data + ;

: respond-read
  0 0 s" QUERY_STRING" param >number 2drop drop { num }
  num 0< num block-count > or if notfound exit then
  num public-block-count < if
    s" HTTP_PASSWD" param passwd passwd# str= 0= if notfound exit then
  then
  ok-octet
  num data-block block-size rtype
;

: respond-write
  0 0 s" QUERY_STRING" param >number 2drop drop { num }
  num 0< num block-count > or if notfound exit then
  s" HTTP_PASSWD" param passwd passwd# str= 0= if notfound exit then
  payload nip block-size <> if notfound exit then
  payload drop num data-block block-size cmove save
  ok-octet
;

set-current ( public )

: respond-storage-read respond-read ;
: respond-storage-write respond-write ;

previous previous
