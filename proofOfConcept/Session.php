<?php
$file = fopen(str_replace(".", "_",$_POST["id"]), "w");
fclose($file);
?>
