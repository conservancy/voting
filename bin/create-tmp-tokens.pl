#!/usr/bin/perl
use DBI;

# Script to create temporary tokens for voters.
#
# How to use this script
# ======================
#
# Look for the elections/referendum id in the database. Like
# "SELECT * FROM elections"
# Look for the current one and remember its id.
#
#
# If don't don't have a row for the current election yet, consider using
# BEGIN; SET NAMES 'utf8';
# INSERT INTO elections (name, voting_start, voting_end, choices_nb, question)
# VALUES ('2010 Spring Board of Directors Election',
#   TIMESTAMP('2009-06-08 00:00:00'), 
#   TIMESTAMP('2009-06-22 23:59:59'),
#   7,
#   'Which candidates would you like to see in the GNOME Foundation Board?');
#
# INSERT INTO election_choices (election_id, choice)
# VALUES ((SELECT LAST_INSERT_ID()), 'Firstname Lastname1'),
# ((SELECT LAST_INSERT_ID()), 'Firstname Lastname2'),
# ((SELECT LAST_INSERT_ID()), 'Youget Theidea');
# And "COMMIT;" if there were no errors. Or "ROLLBACK;" if there were errors.
#
# You should then use this script like this:
# $ ./create-tmp-tokens.pl 1 tokens.txt maildata.txt
#
# where 1 is the elections/referendum id in the database.
#
# tokens.txt now contains SQL statements you can use to create the temporary
# tokens in the database. You can do that with, e.g.
# mysql -h button-back -u username -p foundation < tokens.txt
#
# maildata.txt now contains the data that will be used by mail-instructions.pl
#
# This script assumes, that there is a "electorate" Table which can be a 
# simple VIEW created like this:
# CREATE OR REPLACE VIEW `foundation`.`electorate` AS SELECT  id, firstname, lastname, email FROM `foundation`.`foundationmembers` WHERE DATE_SUB(CURDATE(), INTERVAL 2 YEAR) <= foundationmembers.last_renewed_on;

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


die "Usage: create-tmp-tokens.pl <election id> <output file for tokens> <output file for mail data>\n" unless $#ARGV == 2;

$election_id = $ARGV[0];

open TOKENS, ">$ARGV[1]" || die "Cannot open file $ARGV[1]: $!";
open MAILDATA, ">$ARGV[2]" || die "Cannot open file $ARGV[2]: $!";

my $datasource = "dbi:mysql:foundation:button-back:3306";
my $dbi = DBI->connect ($datasource, 'username', 'password') or die "Unable to connect mysql server: $DBI:errstr\n";

my $query = "SET NAMES 'utf8'";
my $dbh = $dbi->prepare($query);
$dbh->execute();

my $query = "SELECT id,firstname,lastname,email FROM electorate";

my $dbh = $dbi->prepare($query);
$dbh->execute();
$dbh->bind_columns(\$id, \$firstname, \$lastname, \$email);

print TOKENS "SET NAMES 'utf8';\n";
while ($dbh->fetch()) { 
    @chars = ( "A" .. "Z", "a" .. "z", 0 .. 9 );
    $token = join("", @chars[ map { rand @chars } ( 1 .. 10 ) ]);

    print TOKENS "INSERT INTO election_tmp_tokens (election_id, member_id, tmp_token) VALUES ($election_id,$id,'$token');\n";
    print MAILDATA "$firstname $lastname;$email;$token\n";
}

close MEMBERS;
close TOKENS;
close MAILDATA;
