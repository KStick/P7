<?php
$myfile = fopen($_POST["sessionID"], "w");
fwrite($myfile, htmlspecialchars($_POST['data']));
fclose($myfile);

?>
