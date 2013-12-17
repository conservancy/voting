#! /usr/bin/python

import re
import sys
import string

nospam_re = re.compile ("no_spam\.?")

def unmunge_email (addr):
    unmunged = nospam_re.sub ("", addr)
    return unmunged


comment_re = re.compile ("^#.*")
entry_re = re.compile (" *(.*?)<(.*?)> *\((.*?)\) *")

filename = sys.argv[1]

handle = open (filename)

lines = handle.readlines ()

count = 0

for line in lines:
    line = comment_re.sub ("", line)
    string.strip (line)
    if line == "" or line == "\n":
        continue

    match = entry_re.search (line)
    if match:
        name = string.strip (match.group (1))
        email = unmunge_email (string.strip (match.group (2)))
        contribution = string.strip (match.group (3))
        count = count + 1
        print email
    else:
        print "No match: " + line

handle.close ()

