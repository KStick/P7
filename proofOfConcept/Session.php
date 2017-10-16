<?php
if(is_numeric($_POST["sessionID"])){
	$file = fopen($_POST["id"], "w");
	fclose($file);
}
?>
