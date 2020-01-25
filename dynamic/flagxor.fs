#! /usr/bin/env gforth

needs posix.fs
needs scgi.fs
needs iptrack.fs
needs boardtoy.fs

: respond-root
  ok-html
  r\ <!html>
  r\ <h1>Under Construction</h1>
;

: respond
  s" DOCUMENT_URI" param s" /" str= if respond-root exit then
  s" DOCUMENT_URI" param s" /iptrack" str= if respond-iptrack exit then
  s" DOCUMENT_URI" param s" /boardtoy" str= if respond-boardtoy exit then
  notfound
;

' respond 1888 scgi-run
