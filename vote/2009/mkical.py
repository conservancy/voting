#!/usr/bin/env python
'''
This Python script creates a simple iCal file based on hardcoded events
in this file.
'''

import datetime
import logging
import vobject


#### Configure these variables
CANDIDATES_OPENED_DATE    = (2009, 5, 15)
APPLICATIONS_CLOSED_DATE  = (2009, 5, 22)
CANDIDATES_CLOSED_DATE    = (2009, 5, 25)
CANDIDATES_ANNOUNCED_DATE = (2009, 5, 27)
RENEWALS_CLOSED_DATE      = (2009, 6,  1)
VOTING_OPENED_DATE        = (2009, 6,  8)
VOTING_CLOSED_DATE        = (2009, 6, 22)
PRELIMINARY_RESULTS_DATE  = (2009, 6, 24)
CHALLENGE_CLOSED_DATE     = (2009, 6, 30)



### I'm sorry that this functions clutter your calendar-creating experience
### Please scroll down a bit to edit the description texts

#### Application Data
def c(multilinestring):
    '''
    A helper functions which cleans up a multiline string, so that
    it doesn't contain any newlines or multiple whitespaces
    '''
    stripped = [l.strip() for l in multilinestring.splitlines()]
    ret = " ".join (stripped)
    return ret
    
def d(year, month, day):
    '''
    Just a tiny wrapper around datetime.datetime to create a datetime object
    '''
    return datetime.date(year, month, day)



CANDIDATES_OPENED = (
    d(*CANDIDATES_OPENED_DATE),
    'Announcements and list of candidates open',
    c("""If you are a member of the GNOME Foundation and are interested 
    in running for election, you may nominate yourself by sending an 
    e-mail to foundation-announce@gnome.org with your name, e-mail 
    address, corporate affiliation (if any), and a description of why 
    you'd like to serve, before
    %s (23:59 UTC).""" % d(*CANDIDATES_CLOSED_DATE)) + '''
    ''' + c("""    
    You should also send a summary of your candidacy announcement 
    (75 words or less) to elections@gnome.org. If you are not yet a 
    GNOME Foundation member and would like to stand for election, 
    you must first apply for membership and be accepted to be eligible 
    to run. (You may, however, announce your candidacy prior to formal 
    acceptance of your application;
    should your application not be accepted, you will not be included in 
    the list of candidates.)""") + '''
    ''' + c("""
    Elected board members with this election will serve for a period of 
    12 months instead of 18 months.""")
)

APPLICATIONS_CLOSED = (
    d(*APPLICATIONS_CLOSED_DATE),
    'Applications/Renewals closed',
    c("""If you're not a member of the GNOME Foundation or if 
    you need to renew your membership, you have to apply at
    http://foundation.gnome.org/membership/application.php before
    %s (23:59 UTC).
    """ % d(*APPLICATIONS_CLOSED_DATE))
)

CANDIDATES_CLOSED = (
    d(*CANDIDATES_CLOSED_DATE),
    'List of candidates closed',
    CANDIDATES_OPENED[2] # Get the same text again
)

CANDIDATES_ANNOUNCED = (
    d(*CANDIDATES_ANNOUNCED_DATE),
    'List of candidates announced',
    'You may now start to send your questions to the candidates'
)

RENEWALS_CLOSED = (
    d(*RENEWALS_CLOSED_DATE),
    'Renewals Closed',
    c("""If you are a GNOME Foundation member and your membership status
    runs out before %s, you must apply for renewal of your membership status
    before %s.""" % (d(*VOTING_OPENED_DATE), d(*RENEWALS_CLOSED_DATE))
    )
)

VOTING_OPENED = (
    d(*VOTING_OPENED_DATE),
    'Instructions to vote are sent',
    'We introduce a new voting mechanism: Preferential Voting'
)
VOTING_CLOSED = (
    d(*VOTING_CLOSED_DATE),
    'Votes must be returned',
    'Preliminary results are announced on %s' % d(*PRELIMINARY_RESULTS_DATE)
)


PRELIMINARY_RESULTS = (
    d(*PRELIMINARY_RESULTS_DATE),
    'Preliminary results are announced',
    'The preliminary results can be challenged until %s' % d(*CHALLENGE_CLOSED_DATE)
)

CHALLENGE_CLOSED = (
    d(*CHALLENGE_CLOSED_DATE),
    'Challenges to the results closed',
    "If there weren't any challenges, preliminary results are valid"
)




def create_ical(eventlist):
    '''Generates an ical stream based on the list given as eventlist.
    The list shall contain elements with a tuple with a
    (date, string, string) object, serving as date when the event takes place,
    summary and description respectively.
    '''
    log = logging.getLogger('create_ical')

    cal = vobject.iCalendar()
    cal.add('method').value = 'PUBLISH'
    cal.add('calscale').value = 'GREGORIAN'
    cal.add('x-wr-timezone').value = 'UTC'
    
    for (timestamp, summary, description) in eventlist:
        log.debug('creating %s, %s', timestamp, description)
        vevent = cal.add('vevent')
        vevent.add('dtstart').value = timestamp
        vevent.add('dtend').value = timestamp + datetime.timedelta(1)
        vevent.add('summary').value = summary
        vevent.add('description').value = description
    
    stream = cal.serialize()
    return stream



if __name__ == "__main__":

    logging.basicConfig( level=logging.CRITICAL )
    log = logging.getLogger()
    
    eventlist = [
        CANDIDATES_OPENED,
        APPLICATIONS_CLOSED,
        CANDIDATES_CLOSED,
        CANDIDATES_ANNOUNCED,
        RENEWALS_CLOSED,
        VOTING_OPENED,
        VOTING_CLOSED,
        PRELIMINARY_RESULTS,
        CHALLENGE_CLOSED,
    ]

    ical = create_ical( eventlist )
    print ical
