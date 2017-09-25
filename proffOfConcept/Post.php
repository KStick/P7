<?php
$myfile = fopen($_POST["sessionID"], "w");
fwrite($myfile, $_POST['data']);
fclose($myfile);

?>
