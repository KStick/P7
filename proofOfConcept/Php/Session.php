<?php
if(is_numeric($_POST["id"])){
	if(!file_exists(getcwd()."/../Sessions/".$_POST["id"])){
		$file = fopen(getcwd()."/../Sessions/".$_POST["id"], "w");
		fclose($file);
	}
}
?>
