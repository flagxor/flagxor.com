#! /usr/bin/env gforth

needs posix.fs
needs scgi.fs

: respond-root
  ok-html
  r\ <!html>
  r\ <h1>Testing Forth!</h1>
;

: respond
  s" DOCUMENT_URI" param s" /" str= if respond-root exit then
;

' respond 1888 scgi-run
