<?php

$mem_arr = array(
    array("10.128.70.30", "11211"),
    array("10.128.70.30", "11212"),
    array("10.128.70.30", "11213"),
);

ini_set('display_errors', 'On');

foreach($mem_arr as $ma) {
    $ch = curl_init();
    $url = "http://127.0.0.1/memspy.php";
    $post_data = array (
        "ip" => $ma[0],
        "port" => $ma[1],
    );

    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_HEADER, 0);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $post_data);

    $output = curl_exec($ch);
    echo ($output) . '<br />';
}

?>
