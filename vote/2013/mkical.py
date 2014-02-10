#!/usr/bin/env python
'''
This Python script creates a simple iCal file based on hardcoded events
in this file.
'''

import calendar
import datetime
import logging
import math
import os
import vobject


#### Configure these variables
YEAR = 2013
CANDIDATES_OPENED_DATE    = (YEAR, 5,  6)
CANDIDATES_CLOSED_DATE    = (YEAR, 5, 19)
CANDIDATES_ANNOUNCED_DATE = (YEAR, 5, 22)
VOTING_OPENED_DATE        = (YEAR, 5, 26)
VOTING_CLOSED_DATE        = (YEAR, 6,  9)
PRELIMINARY_RESULTS_DATE  = (YEAR, 6, 11)
CHALLENGE_CLOSED_DATE     = (YEAR, 6, 18)



### I'm sorry that these functions clutter your calendar-creating experience
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
    'Announcements and list of candidates opens',
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
    '''
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

VOTING_OPENED = (
    d(*VOTING_OPENED_DATE),
    'Instructions to vote are sent',
    'Please read your email and follow these instructions and submit your vote by %s' % d(*VOTING_CLOSED_DATE)
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


def wraptext(s, width):
    '''Wraps a string @s at @width characters.
    
    >>> wraptext('fooo', 2)
    ['fo','oo']
    '''
    l = len(s)
    nr_frames = int(math.ceil(float(l)/width))
    print nr_frames
    frames = []
    for i in xrange(nr_frames):
        start, end = i*width, (i+1) * width
        frames.append(s[start:end])
        # One could (and prolly should) yield that
    return frames

def ordinal(n):
    n = int(n)
    if 10 <= n % 100 < 20:
        return str(n) + 'th'
    else:
       return  str(n) + {1 : 'st', 2 : 'nd', 3 : 'rd'}.get(n % 10, "th")
                       

def cal_for_month(month, events, width=80, year=datetime.datetime.now().year):
    '''Generates a textual calendar for the @month in @year.
    It will return a string with the calendar on the left hand side and the
    events on the right hand side.
    @events shall be a list with tuples: timestamp, summary, description.
    
    Returns a string with the calendar
    '''
    log = logging.getLogger('cal_for_month')

    cal = calendar.TextCalendar()
    calstrings = cal.formatmonth(year, month, 3).splitlines()

    for (timestamp, summary, description) in events:
        log.debug('creating %s, %s', timestamp, summary)
        year, month, day = timestamp.year, timestamp.month, timestamp.day
        maxwidth = max([len(cs) for cs in calstrings])
        rightwidth = 80 - maxwidth
        for i, line in enumerate(calstrings):
            needles =      (" %d " % day,
                           " %d\n" % day)
            replacement = "(%d)" % day
            # Find the day so that we can highlight it and add a comment
            day_in_week = False
            for needle in needles:
                if needle in line+"\n":
                    # k, this looks a bit weird but we have that corner 
                    # case with the day being at the end of the line 
                    # which in turn will have been split off
                    day_in_week = True
                    break # Set the needle to the found one
            if day_in_week == False: # Nothing found, try next week
                log.debug('Day (%d) not found in %s', day, line)
                continue
            else:
                log.debug('Day (%d) found in %s', day, line)
                new_line = (line+"\n").replace(needle, replacement).rstrip()
                new_line += "   %s (%s)" % (summary, ordinal(day))
                # Replace in-place for two events in the same week
                # FIXME: This has bugs :-( 
                calstrings[i] = new_line
                    
    return os.linesep.join(calstrings)

def create_textcal(eventlist):
    '''Generates a multiline string containing a calendar with the 
    events written on the side
    The list shall contain elements with a tuple with a
    (date, string, string) object, serving as date when the event takes place,
    summary and description respectively.
    '''
    log = logging.getLogger('textcal')
    log.debug('Generating from %s', eventlist)
    months = set(map(lambda x: x[0].month, eventlist))
    year = set(map(lambda x: x[0].year, eventlist)).pop()
    
    final_cal = []
    for month in months:
        events = filter(lambda x: x[0].month == month, eventlist)
        log.debug('Events for %d: %s', month, events)
        month_cal = cal_for_month(month, events, year=year)
        final_cal.append(month_cal)
        
    return os.linesep.join(final_cal)

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser("usage: %prog [options]")
    parser.add_option("-l", "--loglevel", dest="loglevel", help="Sets the loglevel to one of debug, info, warn, error, critical", 
                      default=None)
    parser.add_option("-i", "--ical",
                      action="store_true", dest="ical", default=False,
                      help="print iCal file to stdout")
    parser.add_option("-t", "--textcal",
                      action="store_true", dest="tcal", default=False,
                      help="print textual calendar to stdout")
    (options, args) = parser.parse_args()

    loglevel = {'debug': logging.DEBUG, 'info': logging.INFO,
                'warn': logging.WARN, 'error': logging.ERROR,
                'critical': logging.CRITICAL}.get(options.loglevel, logging.WARN)
    logging.basicConfig( level=loglevel )
    log = logging.getLogger()
    
    eventlist = [
        CANDIDATES_OPENED,
        CANDIDATES_CLOSED,
        CANDIDATES_ANNOUNCED,
        VOTING_OPENED,
        VOTING_CLOSED,
        PRELIMINARY_RESULTS,
        CHALLENGE_CLOSED,
    ]
    
    if not any([options.ical, options.tcal]):
        parser.error("You want to select either ical or textcal output. See --help for details")
    if options.ical:
        ical = create_ical( eventlist )
        print ical
    if options.tcal:
        tcal = create_textcal( eventlist )
        print tcal
