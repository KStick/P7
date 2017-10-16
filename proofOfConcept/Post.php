<?php
if(is_numeric($_POST["sessionID"])){
    $myfile = fopen(getcwd() . "/Sessions/" . $_POST["sessionID"], "w");
    fwrite($myfile, htmlspecialchars($_POST['data']));
    fclose($myfile);
}
?>
