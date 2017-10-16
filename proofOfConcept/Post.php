<?php
if(is_numeric($_POST["sessionID"])){
    $myfile = fopen($_POST["sessionID"], "w");
    fwrite($myfile, htmlspecialchars($_POST['data']));
    fclose($myfile);
}
?>
