<?php

$audio = "Hi";
//$audio = $_POST["audio"];

$output = exec("python ../ML/audioInput.py $audio");

echo $output;



?>
