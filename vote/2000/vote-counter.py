#! /usr/bin/python

import re
import sys
import string
import md5

class Ballot:
    def __init__ (self):
        self.email = 0
        self.member = 0
        self.token = 0
        self.votes = []

    def add_vote (self, name, id):
        self.votes.append ((name, id))

class Candidate:
    def __init__ (self, name, id):
        self.name = name
        self.id = id
        self.count = 0
	self.voters = []
        
candidates = {}

candidate_tuples = [ \
    ("MARTIN BAULIG", 1), \
    ("CHEMA CELORIO", 2), \
    ("KENNETH CHRISTIANSEN", 3), \
    ("RHETT CREIGHTON", 4), \
    ("BART DECREM", 5), \
    ("MIGUEL DE ICAZA", 6), \
    ("CHRISTOPHER GABRIEL", 7), \
    ("JUANTOMAS GARCIA", 8), \
    ("JIM GETTYS", 9), \
    ("BERTRAND GUIHENEUF", 10), \
    ("THOMPSON HAYNER", 11), \
    ("JOHN HEARD", 12), \
    ("JAMES HENSTRIDGE", 13), \
    ("KEVIN KNERR", 14), \
    ("TUOMAS KUOSMANEN", 15), \
    ("GEORGE LEBL", 16), \
    ("ELLIOT LEE", 17), \
    ("RAPH LEVIEN", 18), \
    ("KJARTAN MARAAS", 19), \
    ("MICHAEL MEEKS", 20), \
    ("DAN MUETH", 21), \
    ("ESKIL HEYN OLSEN", 22), \
    ("HAVOC PENNINGTON", 23), \
    ("ETTORE PERAZZOLI", 24), \
    ("BRUCE PERENS", 25), \
    ("LESLIE PROCTOR", 26), \
    ("FEDERICO MENA QUINTERO", 27), \
    ("ARIEL RIOS", 28), \
    ("ARLO ROSE", 29), \
    ("JOE SHAW", 30), \
    ("MACIEJ STACHOWIAK", 31), \
    ("OWEN TAYLOR", 32), \
    ("DANIEL VEILLARD", 33) ]    

for c in candidate_tuples:
    cand = Candidate (c[0], c[1])
    candidates[cand.id] = cand

from_line_re = re.compile ("^From: *(.*)")
member_address_re = re.compile (">? *Member Address: *([^ ]*)")
auth_token_re = re.compile (">? *Validation Token: *(.*)")
vote_re = re.compile (">? *([A-Z ]+) *\(ID# *([0-9]+)\)")

ballots = []
current_ballot = 0

filename = sys.argv[1]      # mail archive file 
secret_cookie = sys.argv[2] # secret cookie
voter_list = sys.argv[3]    # list of valid voter addresses

# hash from valid addresses to whether they have sent in a ballot yet
valid_addresses = {}

voter_handle = open (voter_list)
for voter_addr in voter_handle.readlines ():
    valid_addresses[string.strip (voter_addr)] = 0

handle = open (filename)
lines = handle.readlines ()
for line in lines:

    match = from_line_re.match (line)
    if match:
        email = string.strip (match.group (1))
        if current_ballot:
            ballots.append (current_ballot)
        current_ballot = Ballot ()
        current_ballot.email = email

        continue

    match = member_address_re.match (line)
    if match:
        member = string.strip (match.group (1))
        if (current_ballot.member):
            print "Duplicate member address in ballot from '%s' - duplicates ''%s', '%s'" % (current_ballot.email, current_ballot.member, member)
        else:        
            current_ballot.member = member

        continue
            
    match = auth_token_re.match (line)
    if match:
        token = string.strip (match.group (1))
        if (current_ballot.token):
            print "Duplicate auth token in ballot from '%s' - duplicates '%s', '%s'" % (current_ballot.email, current_ballot.token, token)
        else:
            current_ballot.token = token

        continue

    match = vote_re.match (line)
    if match:
        name = string.strip (match.group (1))
        id = string.strip (match.group (2))

        id = int(id)

        if not candidates.has_key (id):
            print "Unknown candidate '%s' ID %d in ballot from '%s'" % (name, id, current_ballot.email)
        elif not candidates[id].name == name:
            print "Candidate name '%s' for ID '%s' doesn't match, expected '%s'" % (name, id, candidates[id].name)    
        else:
            current_ballot.add_vote (name, id)

        continue
    
if current_ballot:
    ballots.append (current_ballot)    
        
handle.close ()

def contains_dups (b):
    dups = {}
    for v in b.votes:
        id = v[1]
        if dups.has_key (id):
            return 1
        dups[id] = 1
    return 0

dup_tokens = {}
def md5_is_bad (b):
    key = b.member + secret_cookie
    m = md5.new (key)
    digest = m.digest ()
    # convert to hex, python 2.0 has hexdigest() but this one I'm using
    # apparently does not
    token = ""
    for num in digest:
        token = token + ("%02x" % (ord(num),))
    if token == b.token:
        if dup_tokens.has_key (token):
            print "Auth token occurs twice, someone voted more than once"
            return 1
        else:
            dup_tokens[token] = 1
        return 0
    else:
        print "Bad auth token is %s hashed from '%s'" % (token, key)
        return 1

def valid_voter (addr):
    return valid_addresses.has_key (addr)

valid_ballots = {}

i = 0
for b in ballots:
    error = 0
    if not b.member:
        error = "missing member address"
    elif not b.token:
        error = "missing auth token"
    elif len (b.votes) > 11:
        error = "too many votes (%d votes)" % len (b.votes)
    elif len (b.votes) == 0:
        error = "didn't list any candidates"
    elif contains_dups (b):
        error = "contains duplicate votes for the same candidate"
    elif md5_is_bad (b):
        error = "bad authentication token"
    elif not valid_voter (b.member):
        error = "ballot from someone not on the list of valid voters"
    else:
        if valid_ballots.has_key (b.token):
            old = valid_ballots[b.token]
            print "Overriding previous valid ballot %d from %s with new ballot %d" % (old[1], old[0].email, i)
        valid_ballots[b.token] = (b, i)

    if error:
        print "Ignoring ballot %d from '%s' due to: %s" % (i, b.email, error)
        
    i = i + 1

def tupcmp (a, b):
    return cmp (a[1], b[1])

## Print results only after all errors have been printed, so
## we don't lose any errors.
valids = valid_ballots.values ()
valids.sort (tupcmp)
for (b, i) in valids:
    print "Ballot %d:" % i

    print "  From:   " + b.email
    print "  Member: " + b.member
    print "  Token:  " + b.token
    print "  Voted for %d candidates:" % len (b.votes)

    voted_for = []

    valid_addresses[b.member] = 1

    for v in b.votes:
        id = v[1]
        candidates[id].count = candidates[id].count + 1
	candidates[id].voters.append (b.member)
        voted_for.append (candidates[id].name)

    for v in voted_for:
        print "   " + v

print "The following members did not vote:"
for addr in valid_addresses.keys ():
    if not valid_addresses[addr]:
        print addr

def cmpcand (a, b):
    return cmp (a.count, b.count)

cand_list = candidates.values ()
cand_list.sort (cmpcand)

print ""
print ""
print "ELECTION RESULTS:"

print " %d of %d members cast a valid ballot" % (len (valids), len (valid_addresses.keys()))

for c in cand_list:
    print "  %s (%d votes)" % (c.name, c.count)





