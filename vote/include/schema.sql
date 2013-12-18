DROP TABLE IF EXISTS `elections`;
 CREATE TABLE `elections` (
   `id` int(11) NOT NULL auto_increment,
   `type` enum('elections','referendum') NOT NULL default 'elections',
   `name` varchar(150) NOT NULL default '',
   `voting_start` datetime default NULL,
   `voting_end` datetime default '0000-00-00 00:00:00',
   `choices_nb` int(11) NOT NULL default '0',
   `question` text NOT NULL,
   PRIMARY KEY  (`id`));
DROP TABLE IF EXISTS `election_anon_tokens`;
 CREATE TABLE `election_anon_tokens` (
   `id` int(11) NOT NULL auto_increment,
   `anon_token` varchar(200) NOT NULL default '',
   `election_id` int(11) NOT NULL default '0',
   PRIMARY KEY  (`id`)
 ) ENGINE=InnoDB AUTO_INCREMENT=903 DEFAULT CHARSET=utf8;
DROP TABLE IF EXISTS `election_choices`;
 CREATE TABLE `election_choices` (
   `id` int(11) NOT NULL auto_increment,
   `election_id` int(11) NOT NULL default '0',
   `choice` varchar(150) NOT NULL default '',
   PRIMARY KEY  (`id`)
 ) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8 ;
DROP TABLE IF EXISTS `election_tmp_tokens`;
 CREATE TABLE `election_tmp_tokens` (
   `election_id` int(11) NOT NULL default '0',
   `member_id` int(11) NOT NULL default '0',
   `tmp_token` varchar(200) NOT NULL default ''
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* 
from members database we prepare anon tokens
 then insert those anon tokens to database 
 of course before a new election record should be created since its id is needed for anon_tokens
 and election_choices are to be inserted
 rest is handled by itself iirc 
<bolsh> There's "election_votes" and "foundationmembers" too
 I'm not sure if there's a join done between foundationmembers and the other tables
*/

DROP TABLE IF EXISTS `election_votes`;
CREATE TABLE `election_votes` (
   `id` int(11) NOT NULL auto_increment,
   `choice_id` int(11) NOT NULL default '0',
   `anon_id` int(11) NOT NULL default '0',
   PRIMARY KEY  (`id`));

