<?php

function step2_do () {
  global $election;
  global $choices;
  global $vote;
  global $votes_array;

  $result = "<h2>Step 2/4 - Choose your vote</h2>\n";

  $result .= "<p>Choose your candidates in the order of your preference by ";
  $result .= "clicking on them. Don't worry, if you click on someone by mistake ";
  $result .= "you can correct it later. Once you are happy with the order, ";
  $result .= "submit your vote. You will have the chance to review and confirm";
  $result .= " your ballot on the next page.</p>";

  $result .= "<p>You can vote for as few or as many candidates as you choose. ";
  $result .= "Your vote will be counted for your first choice candidate as ";
  $result .= "long as the candidate is still in the race, and when the candidate is eliminated, your ";
  $result .= "vote will transfer to the next preference candidate still in the ";
  $result .= "race.</p>";

  $result .= "<p><noscript>Note: This page requires Javascript</noscript></p>";

  $result .= "<p>Possible choices:</p>\n";

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
