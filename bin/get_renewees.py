#!/usr/bin/env python
"""
This program gets the members from the MySQL Database that need renewal.
By starting with --mode=day you can select only those members that need to
renew today.
With --mode=year you get the members that need to renew this year, i.e. 
whole 2011.

One can send email, too. Use the --send-mail switch to send email.

If you want to test your setup, you can use --one-only=your@address.com to test
whether email actually works or what From address is used, which is
configurable with --from-address=other@address.com.

In order to work properly, you need to have your MySQL client configured 
properly, i.e. ~/.my.cnf should be set up with the appropriate 
credentials:
[client]
host=button-back
user=anonvoting
password=foobar
default-character-set=utf8

The reason to call MySQL client and not use the Python library is 
mainly, that the MySQL bindings are not installed.
"""

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

import datetime
try:
    from email.mime.text import MIMEText
    from email.mime.nonmultipart import MIMENonMultipart
    from email.charset import Charset
except ImportError:
    from email.MIMEText import MIMEText
    from email.Charset import Charset
    from email.MIMENonMultipart import MIMENonMultipart
import logging
from optparse import OptionParser
import smtplib
import StringIO
import subprocess
import sys
import tempfile

__author__ = "Tobias Mueller"
__copyright__ = "Copyright 2011, The GNOME Project"
__credits__ = ["Tobias Mueller",]
__license__ = "GPLv3+"
__version__ = "1.0.0"
__maintainer__ = "Tobias Mueller"
__email__ = "tobiasmue@gnome.org"
                    

TEMPLATE = '''
Dear %(firstname)s,

your GNOME Foundation Membership started on %(last_renewed_on)s.
The term of a membership is two years.
If you want to continue being a member, you have to apply again for
a membership.

Please see https://foundation.gnome.org/membership/apply for details.

Thanks,
  The GNOME Membership and Elections Committee
'''.strip()

log = logging.getLogger()

class MTText(MIMEText):
    def __init__(self, _text, _subtype='plain', _charset='utf-8'):
        if not isinstance(_charset, Charset):
            _charset = Charset(_charset)
        if isinstance(_text,unicode):
            _text = _text.encode(_charset.input_charset)
        MIMENonMultipart.__init__(self, 'text', _subtype,
                                       **{'charset': _charset.input_charset})
        self.set_payload(_text, _charset)


def send_email(to, subject, emailtext, from_address = None, smtp_server = 'localhost'):
    log = logging.getLogger('eMail')
    s = None
    from_address = from_address or "GNOME Membership and Elections Committee <membership-committee@gnome.org>"
    
    msg = MTText(emailtext)
    msg['To'] = to
    msg['From'] = from_address
    msg['Subject'] = subject
    msgstr = msg.as_string()

    if s is None:
        s = smtplib.SMTP()
        s.connect(smtp_server)
    try:
        log.info('Trying to send to %s, %s', to, subject)
        s.sendmail(from_address, [to,], msgstr)
    except smtplib.SMTPException,e :
        log.warning("Error: Could not send to %s!" % (to,))
        raise e

    #if s:
    #    s.quit()
    
class Member(object):
    def __init__(self, firstname, lastname, email, token_or_last_renewed_on):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.token_or_last_renewed_on = token_or_last_renewed_on
        
    @classmethod
    def from_csv(cls, csvstring):
        firstname, lastname, email, token_or_last_renewed_on = csvstring.strip().split(';')
        return Member(firstname, lastname, email, token_or_last_renewed_on)
    
    def __str__(self):
        if False: # string.format is too recent Python
            fmt = "{firstname} {lastname} <{email}> (token_or_last_renewed_on)"
            return fmt.format(self)
        fmt = "%(firstname)s %(lastname)s <%(email)s> (%(token_or_last_renewed_on)s)"
        return fmt % self.__dict__

    def __repr__(self):
        fmt = "<Member <%(email)s> (%(token_or_last_renewed_on)s)>"
        return fmt % self.__dict__



def execute_query(query):
    log.debug('MySQL Query: %s', query)
    DATABASE = "foundation"
    mysql_p = subprocess.Popen(['mysql', DATABASE], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    SQL_result, SQL_error = mysql_p.communicate(query)
    if SQL_error:
        sys.stderr.write('Error Executing SQL: %s' % SQL_error)
    if not SQL_result:
        log.info('NULL Result from SQL')
        infile = StringIO.StringIO("")
    else:
        infile = StringIO.StringIO(SQL_result)
        _ = infile.next() # The first line is garbage, I think it's MySQL output
    return infile

def get_members_which_need_renewal(mode):
    """
    Generates and executes a SQL Query which asks the foundation's database
    for members that need to renew.
    The base date is calculated from the mode argument:
        election:   Last years 07-01 until this years 07-01
        year:       Beginning of the year, i.e. 01.01. until 31.12.
        month:      From 1st of this month to end of this month
        day:        Members that need to renew this day
    """
    ELECTION_FROM_DATE = """CONCAT(
                            YEAR(
                                DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
                            ),
                            '-07-01')
                        """.strip()# Last years July, 1st
    ELECTION_TO_DATE = """CONCAT(YEAR(CURDATE()), '-07-01')""" # This years July, 1st

    DAY_FROM_DATE = """DATE_FORMAT(NOW(),"%Y-%m-%d")"""
    DAY_TO_DATE = DAY_FROM_DATE

    MONTH_FROM_DATE = """DATE_FORMAT(NOW(),"%Y-%m-01")"""
    MONTH_TO_DATE = """LAST_DAY(NOW())"""

    YEAR_FROM_DATE = """DATE_FORMAT(NOW(),"%Y-01-01")"""
    YEAR_TO_DATE = """DATE_FORMAT(NOW(),"%Y-12-31")"""

    (mysql_from_date, mysql_to_date) = {
            'election': (ELECTION_FROM_DATE, ELECTION_TO_DATE),
            'day':      (DAY_FROM_DATE,DAY_TO_DATE),
            'month':    (MONTH_FROM_DATE, MONTH_TO_DATE),
            'year':     (YEAR_FROM_DATE, YEAR_TO_DATE),
        }[mode]
    QUERY = '''
               SET names 'utf8';
               SELECT CONCAT(firstname, ';', lastname, ';', email, ';', last_renewed_on)
               FROM foundationmembers
               WHERE   last_renewed_on >= DATE_SUB(
                         %(mysql_from_date)s ,
                         INTERVAL 2 YEAR
                      )
                    AND last_renewed_on <= DATE_SUB(
                         %(mysql_to_date)s ,
                         INTERVAL 2 YEAR
                       )
               ORDER BY lastname;
            '''.strip()
    QUERY %= {'mysql_from_date': mysql_from_date,
              'mysql_to_date': mysql_to_date}
    infile = execute_query(QUERY)
    memberlist = [Member.from_csv(line.strip()) for line in infile]
    return memberlist

def get_members_election_token(election_id):
    '''
    Execute a SQL query to get a list of members with their temporary election
    token.
    
    The token need to be created first, i.e. using smth like
    
    INSERT INTO election_tmp_tokens (election_id, member_id, tmp_token)
    SELECT @election_id, id, SUBSTRING(MD5(RAND()) FROM 1 FOR 24) AS tmp_token
    FROM electorate;
    '''    
    QUERY = '''
               SET names 'utf8';
               SELECT CONCAT(firstname, ';', lastname, ';', email, ';', tmp_token)
               FROM election_tmp_tokens, foundationmembers
               WHERE election_id = %(election_id)s
                 AND member_id = id;
            '''.strip()
    QUERY %= {'election_id': election_id}
    result = execute_query(QUERY)
    memberlist = [Member.from_csv(line.strip()) for line in result]

    return memberlist

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-l", "--loglevel", dest="loglevel",
                      help="Sets the loglevel to one of debug, info, warn, "
                            "error, critical", default="info")
    parser.add_option("-m", "--mode", dest="mode",
                      help="Which members to get: one of year, month, day, election"
                            " [default: %default]", default="month")
    parser.add_option("-s", "--send-mail", dest="sendmail",
                      help="Do indeed send mail [default: %default]",
                      action="store_true",
                      default=False)
    parser.add_option("-t", "--token", dest="token_for_election",
                      help="Process temporary token, instead of renewals."
                      "Please give the election id, which you should know, as "
                      "argument to this parameter. A program argument is also required"
                      " to read the instructions as a template."
                      "[default: %default]",
                      default=False)
    parser.add_option("-1", "--one-only", dest="oneonlyaddress",
                      help="Send one mail only to this address [default: %default]",
                      default=None)
    parser.add_option("-f", "--from-address", dest="fromaddress",
                      help="Use that as sending address [default: %default]",
                      default="Tobias Mueller <tobiasmue@gnome.org>")
    (options, args) = parser.parse_args()
    loglevel = {'debug': logging.DEBUG, 'info': logging.INFO,
                'warn': logging.WARN, 'error': logging.ERROR,
                'critical': logging.CRITICAL}.get(options.loglevel, "warn")
    LOGFORMAT = "%(asctime)s %(levelname)-8s %(name)s %(message)s"
    DATEFORMAT = '%Y-%m-%d %H:%M:%S'
    logging.basicConfig(level=loglevel, format=LOGFORMAT, datefmt=DATEFORMAT)
    log = logging.getLogger('main')
    
    if not options.token_for_election: # This is the default. We care about renewals
        email_subject = 'Your GNOME Foundation Membership is about to expire'
        logmsg = 'Needs Renewal: %s, %s, %s, %s'
        template = TEMPLATE
        members = get_members_which_need_renewal(options.mode)
    else: # This is with -t option. We process election tokens.
        email_subject = 'GNOME Foundation Board of Directors Elections %d - Voting Instructions' % datetime.date.today().year
        logmsg = 'Sending Token: %s, %s, %s, %s'
        template = open(args[0], "r").read()
        members = get_members_election_token(options.token_for_election)
        
        

    if options.oneonlyaddress:
        members = [Member("firstname", "lastname", 
                          options.oneonlyaddress, "2000-05-23")]
        
    
    for member in members:
        firstname, lastname, email, token_or_last_renewed_on = member.firstname, member.lastname, member.email, member.token_or_last_renewed_on
        log.warn(logmsg, lastname, firstname, email, token_or_last_renewed_on)
        emailtext = template % {'firstname':firstname, 'lastname':lastname,
                                 'email': email, 'token_or_last_renewed_on': token_or_last_renewed_on,
                                 'token': token_or_last_renewed_on,
                                 'last_renewed_on': token_or_last_renewed_on,
                               }
        log.debug('The email to be sent is: %s', emailtext)
        to = email
        fromaddress = options.fromaddress
        subject = email_subject
        try:
            if options.sendmail or options.oneonlyaddress:
                send_email(to, subject, emailtext, fromaddress)
        except smtplib.SMTPException,e :
            log.error('Error sending to %s: %s', to, e)
            try:
                tfile = tempfile.NamedTemporaryFile(delete=False)
            except TypeError:
                tfile = tempfile.NamedTemporaryFile()
            tfile.writeline('To: %s' % to)
            tfile.writeline('Subject: %s' % subject)
            tfile.writeline('')
            tfile.writeline('%s' % emailtext)
            log.critical('eMail put in %s', tfile.name)
