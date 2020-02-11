needs posix.fs

get-current vocabulary synch also synch definitions ( private )

0 4096 PROT_READ PROT_WRITE or
  MAP_SHARED MAP_ANONYMOUS or -1 0 mmap constant sync-shared

: guard ( -- a ) sync-shared ;
: waiting ( -- a ) sizeof(sem_t) sync-shared + ;
: waking ( -- a ) sizeof(sem_t) 2* sync-shared + ;
: waiters ( -- n ) sizeof(sem_t) 3 * sync-shared + ;

0 waiters !
guard 1 1 sem_init throw
waiting 1 0 sem_init throw
waking 1 0 sem_init throw

: awake
  guard sem_wait throw
  waiters @ 0 waiters !
  0 ?do waiting sem_post throw 
        waking sem_wait throw loop
  guard sem_post throw
;

: await
  guard sem_wait throw
  1 waiters +!
  guard sem_post throw
  waiting sem_wait throw
  waking sem_post throw
;

set-current ( public )

: awake awake ;
: await await ;

previous

