#!/usr/bin/env python

import datetime
import logging
from optparse import OptionParser
from textwrap import dedent
import sys

from get_renewees import get_members_which_need_renewal, send_email

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__ = "Tobias Mueller"
__license__ = "GPLv3+"
__email__ = "tobiasmue@gnome.org"

TEMPLATE = dedent('''
    Hi,
     
    as per point 1.3 of [1], here it comes a list of members in need of a
    renew in case they didn't receive their individual e-mail:
     
    First name, Last name (Last renewed on)
    %(members)s
     
    The Renewal form can be found at [2].
     
    Cheers,
      GNOME Membership and Elections Committee
     
    [1] https://mail.gnome.org/archives/foundation-list/2011-November/msg00000.html
    [2] http://www.gnome.org/foundation/membership/apply/

''')

def format_members_for_mail(members, template=TEMPLATE):
    fmt = " * %(firstname)s, %(lastname)s (%(token_or_last_renewed_on)s)"
    member_lines = [fmt % member.__dict__ for member in members]

    members_formatted = '\n'.join(member_lines)

    mail = template % {'members': members_formatted}
    
    return mail
    
def main(options=None):
    log = logging.getLogger()

    options = options or {}
    if options:
        if options.template:
            template = open(options.template, 'r').read()
        else:
            template = TEMPLATE
        
        if options.recipient:
            to = options.recipient
        else:
            to = 'foundation-list@gnome.org'

        if options.sendmail:
            sendmail = options.sendmail
        else:
            sendmail = False



    members = get_members_which_need_renewal('month')
    if not members:
        log.warn('No one needs renewals! :-)')
    
    else: # We do have members
        emailtext = format_members_for_mail(members)
        
        today = datetime.date.today()
        subject = "Memberships needing renewal (%s)" % today.strftime("%02Y-%02m")
        
        if sendmail:
            log.warn('Sending mail to %s: %s', to, subject)
            send_email(to, subject, emailtext)
        else:
            log.info('Not sending mail to %s', to)
            log.info('%s', subject)
            log.info('%s', emailtext)
    
    return 0
    
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-f", "--from-address", dest="fromaddress",
                      help="Use that as sending address [default: %default]",
                      default="Tobias Mueller <tobiasmue@gnome.org>") 
    parser.add_option("-s", "--send-mail", dest="sendmail",
                      help="Do indeed send mail [default: %default]",
                      action="store_true",
                      default=False)
    parser.add_option("-l", "--loglevel", dest="loglevel",
                      help="Sets the loglevel to one of debug, info, warn, "
                            "error, critical", default="info") 
    parser.add_option("-r", "--recipient", dest="recipient",
                      help="Address to send an email to",
                            default=None) 
    parser.add_option("-t", "--template", dest="template",
                      help="Use this file as a template, instead of the "
                            "hardcoded default one. "
                            "Please look at the source to see the available "
                            "variables.",
                            default=None) 
    (options, args) = parser.parse_args()
    loglevel = {'debug': logging.DEBUG, 'info': logging.INFO,
                'warn': logging.WARN, 'error': logging.ERROR,
                'critical': logging.CRITICAL}.get(options.loglevel, "warn")
    LOGFORMAT = "%(asctime)s %(levelname)-8s %(name)s %(message)s"
    DATEFORMAT = '%Y-%m-%d %H:%M:%S'
    logging.basicConfig(level=loglevel, format=LOGFORMAT, datefmt=DATEFORMAT)
    log = logging.getLogger('main')

    sys.exit (main (options))
     
