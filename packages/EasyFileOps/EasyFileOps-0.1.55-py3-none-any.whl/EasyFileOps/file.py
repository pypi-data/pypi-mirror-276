# Thanks for using EasyFileOps
# I hope this will help you work
# Some options returns specified data, check code or read documentation

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


def seek_config(seek):
    try:
        seek_pos = (int(seek))
    except (TypeError, ValueError) as e:
        seek_pos = 0
        print(e, " Error, Seek changed to 0")
    return seek_pos


def file(filename, option, towrite='', seek=0):
    try:
        # r options
        if option in ['r', 'r+', 'rb', 'rb+']:
            with open(filename, option) as f:
                if option in ['r+', 'rb+']:
                    seek_pos = seek_config(seek)
                    f.seek(seek_pos)
                    if option == 'r+':
                        try:
                            f.write(str(towrite))
                        except TypeError as e:
                            print(e)
                    elif option == 'rb+':
                        try:
                            if isinstance(towrite, bytes):
                                f.write(towrite)
                            else:
                                f.write(towrite.encode())
                        except (TypeError, AttributeError) as e:
                            print(e)
                f.seek(0)
                read = f.read()
                lines = read.splitlines()
                print("Done")
                return read, lines
        # w options
        elif option in ['w', 'w+', 'wb', 'wb+']:
            with open(filename, option) as f:
                seek_pos = seek_config(seek)
                f.seek(seek_pos)
                if option in ['wb', 'wb+']:
                    try:
                        if isinstance(towrite, str):
                            f.write(towrite.encode())
                        elif isinstance(towrite, bytes):
                            f.write(towrite)
                    except TypeError as e:
                        print(e)
                else:
                    try:
                        f.write(str(towrite))
                    except TypeError as e:
                        print(e)
                print(f"Saved")
        # a options
        elif option in ['a', 'a+', 'ab', 'ab+']:
            with open(filename, option) as f:
                if option in ['ab+', 'ab']:
                    try:
                        if isinstance(towrite, str):
                            f.write(towrite.encode())
                        elif isinstance(towrite, bytes):
                            f.write(towrite)
                    except TypeError as e:
                        print(e)
                else:
                    try:
                        f.write(str(towrite))
                    except TypeError as e:
                        print(e)
                return print(f"Saved")
        # read option
        elif option == "read":
            with open(filename, "r") as f:
                read = f.read()
                print("Done")
                return read
        # readline option
        elif option == "readline":
            with open(filename, "r") as f:
                readline = f.readline()
                print("Done")
                return readline
        # readlines option
        elif option == "readlines":
            with open(filename, "r") as f:
                lines = f.readlines()
                print("Done")
                return lines
        # splitlines option
        elif option == "splitlines":
            with open(filename, "r") as f:
                lines = f.read().splitlines()
                print("Done")
                return lines
        # split options
        elif option == "split":
            with (open(filename, "r") as f):
                split = f.read()
                words = split.split()
                print("Done")
                return words
        # readable option
        elif option == "readable":
            with open(filename, towrite) as f:
                check = f.readable()
                if check is True:
                    print("File is readable")
                else:
                    print("File not readable")
        # seekable option
        elif option == "seekable":
            with open(filename, towrite) as f:
                check = f.seekable()
                if check is True:
                    print("File is seekable")
                else:
                    print("File not seekable")
        # writable option
        elif option == "writable":
            with open(filename, towrite) as f:
                check = f.writable()
                if check is True:
                    print("File is writable")
                else:
                    print("File not writable")
        # truncate option
        elif option == "truncate":
            with open(filename, 'r+') as f:
                f.truncate(int(towrite))
                print("File truncated to: ", towrite, " bytes")
        # fileno option
        elif option == "fileno":
            with open(filename, "r") as f:
                pos = f.fileno()
                print("File descriptor: ", pos)
        # flush option
        elif option == "flush":
            with open(filename, "r") as f:
                f.flush()
                print("Flushed")
        # isatty option
        elif option == "isatty":
            with open(filename, "r") as f:
                check = f.isatty()
                if check is True:
                    print("File stream is interactive")
                else:
                    print("File stream is not interactive")
        # detach option
        elif option == "detach":
            with open(filename, towrite) as f:
                de = f.detach()
                print("File detached: ", de)
        # writelines option
        elif option == 'writelines':
            with open(filename, 'w+') as f:
                seek_pos = seek_config(seek)
                f.seek(seek_pos)
                lines = towrite
                for line in lines:
                    f.write(line + '\n')
                print("Saved")
    except (FileNotFoundError, ValueError, TypeError, UnicodeDecodeError, MemoryError, IOError, PermissionError, BufferError, AttributeError) as e:
        print(e)
    finally:
        try:
            f.close()
        except (UnboundLocalError, ValueError):
            pass
    return None
