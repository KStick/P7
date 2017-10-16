<?
session_start();
	$username = $_POST['username'];
	$text = $_POST['text'];
	$sessionID = $_POST['sessionID'];
	$fp = fopen("SessionsChatlogs/" . $sessionID . ".html", 'a');
	fwrite($fp, "<div class='msgln'>(".date("G:i").") <b>".$username."</b>: ".stripslashes(htmlspecialchars($text))."<br></div>");
	fclose($fp);
?>
