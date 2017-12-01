<?php
session_start();
ini_set('display_errors', 'On');
error_reporting(E_ALL | E_STRICT);
	$username = $_POST['username'];
	$text = $_POST['text'];
	$sessionID = $_POST['sessionID'];
	if(is_numeric($_POST["sessionID"])){
		$fp = fopen( getcwd() .  "/SessionsChatlogs/" . $sessionID . ".html", "a");
		error_log("this is a test");
		error_log($username . $text . $sessionID);
		error_log(error_get_last());
		fwrite($fp, "<div class='msgln'>(".date("G:i").") <b>".$username."</b>: ".stripslashes(htmlspecialchars($text))."<br></div>");
		fclose($fp);
		$_SESSION["test"] = error_get_last();
		$_SESSION["kenneth"] = "kenneth er en cunt";
	}
?>
