<?
session_start();
ini_set('display_errors', 'On');
error_reporting(E_ALL | E_STRICT);
	$username = $_POST['username'];
	$text = $_POST['text'];
	$sessionID = $_POST['sessionID'];
	$print = $username . $sessionID . $text;
	echo "test";
	if(is_numeric($_POST["sessionID"])){
		$fp = fopen( getcwd() .  "/SessionsChatlogs/" . $sessionID . ".html", 'a');
		fwrite($fp, "<div class='msgln'>(".date("G:i").") <b>".$username."</b>: ".stripslashes(htmlspecialchars($text))."<br></div>");
		fclose($fp);
	}
?>
