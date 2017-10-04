<?
session_start();
	$username = $_POST['username'];
	$text = $_POST['text'];
	$fp = fopen("log.html", 'a');
	fwrite($fp, "<div class='msgln'>(".date("G:i").") <b>".$username."</b>: ".stripslashes(htmlspecialchars($text))."<br></div>");
	fclose($fp);
?>
