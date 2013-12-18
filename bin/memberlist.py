#!/usr/bin/env python
'''Prints the current member list as JSON'''

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


try:
    import json
except ImportError:
    import simplejson as json

from get_renewees import execute_query, Member

__author__ = "Tobias Mueller"
__license__ = "GPLv3+"
__email__ = "tobiasmue@gnome.org"

query = ("SET NAMES 'utf8'; "
         "SELECT CONCAT(firstname, ';', lastname, ';', email, ';', "
         "              last_renewed_on) "
         " FROM foundationmembers"
         " WHERE DATE_SUB(CURDATE(), INTERVAL 2 YEAR) <= last_renewed_on"
         " ORDER BY lastname, firstname")
      

def get_current_electorate():
    infile = execute_query(query)
    memberlist = [Member.from_csv(line.strip()) for line in infile]

    return memberlist
            

def get_json_memberlist():
    members = get_current_electorate()
    objects = [
        {'firstname': o.firstname,
         'lastname': o.lastname,
         'email': o.email,
         'last_renewed_on': o.token_or_last_renewed_on,
        }
        for o in members]
    
    j = json.dumps(objects, indent=4)
    return j

if __name__ == '__main__':
    print get_json_memberlist()
