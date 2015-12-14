<?php

error_reporting(E_ALL ^ E_NOTICE ^ E_WARNING);

function mem_spy($ip, $port)
{
    $mem = new Memcache;

    //CONNECT
    $c = $mem->connect($ip, $port, 5);
    if(!$c)
    {
        exit('|1|connect to memcache '."$ip".' '."$port".' failed');
    }
    else
    {
        //SET
        $s = $mem->set('spy_key', '|0|memcache '."$ip".' '."$port".' connected!', 0, 60);
        if(!$s)
        {
            exit('|1|set key to '."$ip".' '."$port".' failed!');
        }
        //GET
        $val = $mem->get('spy_key');
        return $val;
        $mem->close();
    }
}

//

if(!isset($_POST['ip']) || !isset($_POST['port'])){
    exit('arguments error.');
}
$reslt = mem_spy($_POST['ip'], $_POST['port']);
//
//

if(!preg_match("\|/1\|/", $reslt))
{
    echo "|0|connect to memcache succeed!";
}

?>
