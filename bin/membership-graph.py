#!/usr/bin/env python
'''
Simple script which takes CSV Data either from stdin or a given filename and plots a graph out of that.
You might want to retrieve CSV Data by executing the following command:

mysql -h button-back -u anonvoting -p foundation -B -e 'SELECT DATE_FORMAT(first_added, "%Y-%m") AS date, COUNT(*) as joined FROM foundationmembers GROUP BY date;' | sed 's/\t/","/g;s/^/"/;s/$/"/;s/\n//g' | awk 'FNR>1'

mysql -h button-back -u anonvoting -p foundation -B -e "SET @start = '2009-01-01', @end = '2009-08-30'; SELECT DATE_FORMAT(DATE_ADD(last_renewed_on, INTERVAL 2 YEAR), '%Y-%m') as date, COUNT(*) as dropped_out FROM foundationmembers WHERE last_renewed_on >= DATE_SUB(@start, INTERVAL 2 YEAR) AND last_renewed_on <= DATE_SUB(@end, INTERVAL 2 YEAR) GROUP BY date;"  | sed 's/\t/","/g;s/^/"/;s/$/"/;s/\n//g' | awk 'FNR>1'
'''

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

import logging
import pylab
from pylab import figure, title, bar, xticks, yticks, gca, savefig
import sys

__author__ = "Tobias Mueller"
__license__ = "GPLv3+"
__email__ = "tobiasmue@gnome.org"

plot_title = "New Foundation Members"
figwidth = 40
figheight = 3

def bar_date_graph(name_value_dict, graph_title="", output_name="bargraph.png", show=False):
  fig = figure(
               #figsize=(figwidth, figheight)
               )

  title(graph_title,
        #size="x-small"
        )

  sortedkeys, sortedvalues = zip(*sorted(zip(name_value_dict.keys(),
                                 name_value_dict.values()), reverse=False))
  for i, value in zip(range(len(sortedvalues)), sortedvalues):
      bar(i + 0.25, value, color="#73d216")

  pylab.xticks(pylab.arange(0.65, len(sortedkeys)),
        [("%s: %d" % (name, value))
          for name, value in zip(sortedkeys, sortedvalues)],
          #size="xx-large",
          )

  yticks(
         #size="xx-large"
         )

  gca().yaxis.grid(which="major")

  fig.autofmt_xdate()

  savefig(output_name)
  
  if show:
      pylab.show()

def normalize(*args):
    out = []
    for a in args:
        cleaned = a.strip(' "')
        #cleaned = int(a)
        out.append(cleaned)
        
    return out

if __name__=="__main__":
    from optparse import OptionParser
    parser = OptionParser("usage: %prog [options] INFILE")
    parser.add_option("-l", "--loglevel", dest="loglevel",
                      help="Sets the loglevel to one of debug, info, warn,"
                      " error, critical", default="error")
    parser.add_option("-o", "--output",
                      dest="output", default="bargraph.png",
                      help="file to create with the plotted graph")
    parser.add_option("-s", "--show",
                      dest="show", default="False", action="store_true",
                      help="display the graph after it has been drawn")
    parser.add_option("-t", "--title",
                      dest="title", default="New Foundation Members",
                      help="set the title of the graph")

    (options, args) = parser.parse_args()
    loglevel = {'debug': logging.DEBUG, 'info': logging.INFO,
                 'warn': logging.WARN, 'error': logging.ERROR,
             'critical': logging.CRITICAL}.get(options.loglevel, "error")
    logging.basicConfig(level=loglevel)
    log = logging.getLogger("MembershipGraph Main")

    output_fname = options.output

    if len(args) > 0:
        fname = args[0]
        if fname == '-':
            infile = sys.stdin
        else:
            infile = file(fname, 'r')
    else:
        path = sys.stdin
        
    
    
    
    values = {}
    date = None
    first = None
    
    lines = infile.readlines()
    for line in lines:
      l = line.strip().split(",")
      if l and l[0] and l[1]:
          x, y = normalize(l[0], l[1])
          print x, y
          if not first:
              first = x
          last = x
          values[x] = int(y)
    
    date = first
    while date != last:
      year, month = date.split("-")
      month = int(month)
      year = int(year)
      month += 1
      if month > 12:
        month = 1
        year += 1
    
      date = "-".join([str(year), str('%02d' % month)])
    
      if date not in values:
        values[date] = 0
    
    bar_date_graph(values, options.title, output_fname, show=options.show)
