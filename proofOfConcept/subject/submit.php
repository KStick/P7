<?php
	$username = $_POST['username'];
	$subject = $_POST['subject'];
	$question = $_POST['question'];
	$filename = "log.txt";
	$fp = fopen($filename, 'a');
	fwrite($fp, $subject."_".$username."_".$question."_".date("d-m-Y-G:i")."_");
	fclose($fp);
?>