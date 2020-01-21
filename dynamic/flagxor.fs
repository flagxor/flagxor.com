#! /usr/bin/env gforth

needs posix.fs
needs scgi.fs
needs iptrack.fs

: respond-root
  ok-html
  r\ <!html>
  r\ <h1>Under Construction</h1>
;

: respond
  s" DOCUMENT_URI" param s" /" str= if respond-root exit then
  s" DOCUMENT_URI" param s" /iptrack" str= if respond-iptrack exit then
  notfound
;

' respond 1888 scgi-run
