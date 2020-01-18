c-library posix26

\c #include <errno.h>
\c #include <fcntl.h>
\c #include <netinet/in.h>
\c #include <semaphore.h>
\c #include <signal.h>
\c #include <sys/mman.h>
\c #include <sys/socket.h>
\c #include <sys/stat.h>
\c #include <sys/types.h>
\c #include <sys/wait.h>
\c #include <time.h>
\c #include <unistd.h>

s" pthread" add-lib

c-function pipe_ pipe a -- n
c-function getpid getpid -- n
c-function fork fork -- n

c-function waitpid waitpid n a n -- n
\c #define wnohang() WNOHANG
c-function WNOHANG wnohang -- n

c-function execl1 execl a a a -- n
c-function execl2 execl a a a a -- n
c-function execl3 execl a a a a a -- n

c-function open open a n n -- n
c-function write write n a n -- n
c-function read read n a n -- n
c-function close close n -- n
c-function ftruncate ftruncate n n -- n

\c #define errno_() errno
c-function errno errno_ -- n

\c #define o_rdwr() O_RDWR
c-function O_RDWR o_rdwr -- n
\c #define o_creat() O_CREAT
c-function O_CREAT o_creat -- n
\c #define o_noctty() O_NOCTTY
c-function O_NOCTTY o_noctty -- n
\c #define o_nonblock() O_NONBLOCK
c-function O_NONBLOCK o_nonblock -- n

\c int bind_helper(int port) {
\c   struct sockaddr_in address;
\c   int opt = 1;
\c   int fd = socket(AF_INET, SOCK_STREAM, 0);
\c   setsockopt(fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt));
\c   address.sin_family = AF_INET; 
\c   address.sin_addr.s_addr = INADDR_ANY; 
\c   address.sin_port = htons(port);
\c   if (bind(fd, (struct sockaddr *)&address, sizeof(address))) {
\c     close(fd);
\c     return -1;
\c   }
\c   return fd;
\c }

\c int accept_helper(int fd) {
\c   struct sockaddr_in address;
\c   int addrlen = sizeof(address);
\c   return accept(fd, (struct sockaddr *)&address, &addrlen);
\c }

\c int connect_helper(int port) {
\c   struct sockaddr_in address;
\c   int fd = socket(AF_INET, SOCK_STREAM, 0);
\c   address.sin_family = AF_INET; 
\c   address.sin_addr.s_addr = INADDR_ANY; 
\c   address.sin_port = htons(port);
\c   if (connect(fd, (struct sockaddr *)&address, sizeof(address))) {
\c     close(fd);
\c     return -1;
\c   }
\c   return fd;
\c }

c-function connect connect_helper n -- n
c-function bind bind_helper n -- n
c-function listen listen n n -- n
c-function sockaccept accept_helper n -- n

\c #define prot_read() PROT_READ
c-function PROT_READ prot_read -- n
\c #define prot_write() PROT_WRITE
c-function PROT_WRITE prot_write -- n
\c #define prot_exec() PROT_EXEC
c-function PROT_EXEC prot_exec -- n

\c #define map_shared() MAP_SHARED
c-function MAP_SHARED map_shared -- n
\c #define map_private() MAP_PRIVATE
c-function MAP_PRIVATE map_private -- n
\c #define map_anonymous() MAP_ANONYMOUS
c-function MAP_ANONYMOUS map_anonymous -- n
\c #define ms_sync() MS_SYNC
c-function MS_SYNC ms_sync -- n
\c #define ms_async() MS_ASYNC
c-function MS_ASYNC ms_async -- n

c-function mmap mmap a n n n n n -- a
c-function munmap munmap a n -- n
c-function msync msync a n n -- n

c-function sem_init sem_init a n n -- n
c-function sem_destroy sem_destroy a -- n
c-function sem_wait sem_wait a -- n
c-function sem_trywait sem_trywait a -- n
c-function sem_timedwait sem_timedwait a a -- n
c-function sem_post sem_post a -- n

\c #define size_timespec() sizeof(struct timespec)
c-function sizeof(timespec) size_timespec -- n
\c void set_timespec(time_t s, long ns, struct timespec *t) {
\c   clock_gettime(CLOCK_REALTIME, t);
\c   t->tv_sec += s;
\c   t->tv_nsec += ns;
\c   if (t->tv_nsec >= 1000000000) {
\c     t->tv_nsec -= 1000000000;
\c     ++t->tv_sec;
\c   }
\c }
c-function timespec! set_timespec n n a -- void

\c #define size_sem_t() sizeof(sem_t)
c-function sizeof(sem_t) size_sem_t -- n

c-function signal signal n a -- a
\c #define SIGPIPE_() SIGPIPE
c-function SIGPIPE SIGPIPE_ -- a
\c #define SIGCHLD_() SIGCHLD
c-function SIGCHLD SIGCHLD_ -- a
\c #define SIG_IGN_() SIG_IGN
c-function SIG_IGN SIG_IGN_ -- a

end-c-library

create pipe_buf 8 allot
: pipe ( -- in out ) pipe_buf pipe_ throw pipe_buf 4 + l@ pipe_buf l@ ;

( utilities )
variable writebuf_
: femit >r writebuf_ c! r> writebuf_ 1 write drop ;
: fcrlf 13 over femit 10 swap femit ;
: octal 8 base ! ;
: sz over + 1- 0 swap c! ;

