"""
###
DOCUMENTATION OF EasyFileOps
###
###
You can install EasyFileOps via pip:
pip install EasyFileOps
###
###
Importing:
from EasyFileOps import file as efo (or any name you want)
###
###
EasyFileOps main method is file
Parameters of file:
filename (str) - Here write a file name to operate on
option (str) - Available options: r, r+, rb, rb+, readline, readlines, readable, w, w+, wb, wb+, writelines, writable,
a, a+, ab, ab+, seekable, flush, detach, fileno, truncate, isatty, split, splitlines
towrite (str or bytes (optional)) - Content to write in operating file
seek (int (optional)) - Position in operating file before performing the operation
###
###
EasyFileOps can return:
options r, r+, rb and rb+:
-read: whole file is read
-splitlines: lines in file
option read:
-read: whole file is read
option readline:
-readline: return one line of file
option readlines:
-lines: return lines of file
option splitlines:
-lines: return lines of file
option split:
-words: return words in file
###
###
Example usages

#Reading entire content of file
content, lines = efo.file("example.txt", "r")

#Wrinting content to a file
efo.file("example.txt", "w", "Hi EasyFileOps!")

#or writing with seek
efo.file("example.txt", "w", "Hi EasyFileOps!", 8)

#Truncate
efo.file("example.txt", "truncate", 40)
###
###
IMPORTANT!!!
if you use these options: seekable, writable, readable, truncate or detach constructions changes:
-for seekable, writable, readable: file("example.txt", "seekable, writable or readable option", "option any with r, w or a")
-for truncate: file("example.txt", "truncate", "(bytes in int)")
-for detach: file("example.txt", "detach", "option any with r, w or a")
###
"""