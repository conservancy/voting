<?php

function step2_do () {
  global $election;
  global $choices;
  global $vote;
  global $votes_array;

  $result = "<h2>Step 2/4 - Choose your vote</h2>\n";

  $result .= "<p>You can vote for as few or as many candidates as you choose. ";
  $result .= "An <a href=\"http://en.wikipedia.org/wiki/Single_transferable_vote\">STV algorithm</a> will be used to count your votes.</p>";

  $result .= "<p>Clicking on a candidate in the <em>Candidates</em> box adds it in order to the Prefences box.  ";
  $result .= "If you want to change a selection you've already made, you can click on the candidate in the <em>Preferences</em> box, and that candidate will move back to the <em>Candidates</em> box.  (Note: you may need to scroll down to see the <em>Preferences</em> box).</p>";
  $result .= "<p>Once you have a <em>Preferences</em> box that you like, use the button at the bottom to continue to the next step.  You can review and confirm";
  $result .= " your ballot on the next page.</p>";

  $result .= "<p><noscript>Note: This page requires Javascript</noscript></p>";

  $result .= '<table>';
  $result .= '  <tr>';
  $result .= '    <td class="canddata"><h3>Candidates</h3><ul id="candidates"></ul></td>';
  $result .= '    <td class="prefdata"><h3>Preferences</h3><ol id="preferences"></ol></td>';
  $result .= '  </tr>';
  $result .= '</table>';

  return $result;
}

?>
