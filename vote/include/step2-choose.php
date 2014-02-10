<?php

function step2_do () {
  global $election;
  global $choices;
  global $vote;
  global $votes_array;

  $result = "<h2>Step 2/4 - Choose your vote</h2>\n";

  $result .= "<p>Clicking on a candidate in the Candidates box adds it in order to the Prefences box.";
  $result .= "If you make an incorrect selection, click on the candidate in the Preferences box, and it will move back to the Candidates box.  Note: you may need to scroll down to see the Preferences box.</p>";
  $result .= "Once you have a Preferences box that you like, use the button at the bottom to continue to the next step.  You can review and confirm";
  $result .= " your ballot on the next page.</p>";

  $result .= "<p>You can vote for as few or as many candidates as you choose. ";
  $result .= "An <a href=\"http://en.wikipedia.org/wiki/Single_transferable_vote\">STV algorithm</a> will be used to count your votes.</p>";

  $result .= "<p><noscript>Note: This page requires Javascript</noscript></p>";

  $result .= "<div class=\"canddata\">\n";
  $result .= "<h3>Candidates</h3>\n";
  $result .= "<ul id=\"candidates\">\n";
  $result .= "</ul>\n";
  $result .= "</div>";
  $result .= "<div class=\"prefdata\">";
  $result .= "<h3>Preferences</h3>\n";
  $result .= "<ol id=\"preferences\">\n";
  $result .= "</ol>\n";

  $result .= "</div>\n";

  return $result;
}

?>
