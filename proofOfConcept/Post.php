<?php
$myfile = fopen(str_replace(".", "_", $_POST["sessionID"]), "w");
fwrite($myfile, htmlspecialchars($_POST['data']));
fclose($myfile);

?>
