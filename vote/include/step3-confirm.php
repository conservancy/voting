<?php

function step3_do () {
  global $election;
  global $choices;
  global $vote;
  global $votes_array;

  $result = "<h2>Step 3/4 - Confirm your vote</h2>\n";

  $result .= "<p><strong>".htmlspecialchars($election["question"])."</strong></p>\n";
  if (count ($votes_array) >= 1) {
    $result .= "<p>You choose to vote for:</p>\n";

    $result .= "<div class=\"votedata\">\n";
    $result .= "<ol>\n";
    foreach ($votes_array as $vote) {
      $found = FALSE;
      foreach ($choices as $choice) {
        if ($choice["id"] == $vote) {
          $result .= "<li>".htmlspecialchars($choice["choice"])."</li>\n";
          $found = TRUE;
          break;
        }
      } 

      if (!$found) {
        $result .= "<li>Unknown vote: ".htmlspecialchars($vote)."</li>\n";
        $error .= "There was an unkown vote: ".htmlspecialchars($vote)."<br />\n";
      }
    }
    $result .= "</ol>\n";

    $result .= "</div>\n";

  } else {
    $result .= "<div class=\"votedata\">\n";
    $result .= "<p>You choose to vote for none of the possible answers.</p>\n";
    $result .= "</div>\n";
  }

  $result .= "<p>To confirm this vote, please continue to the next step. ";
  $result .= "To modify your choice, hit the \"Back\" button in your browser.</p>\n";

  return $result;
}

?>
