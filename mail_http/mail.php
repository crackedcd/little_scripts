<html>
<head><meta http-equiv='Content-Type' content='text/html; charset=utf-8'></head>
<body>

<?php

if(isset($_POST["sub"]) && isset($_POST["content"]) && isset($_POST["to_addr"])) {
    $mail_subject = $_POST["sub"];
    $mail_content = $_POST["content"];
    $to_list = $_POST["to_addr"];

    require "smtp.php";
    $smtpserver = "10.1.6.4";
    $smtpserverport =25;
    $smtpusermail = "alarm@yyzcb.com";
    //$smtpemailto = "$mail_to";
    $smtpuser = "usr";
    $smtppass = "pwd";
    $mailsubject = mb_convert_encoding($mail_subject, "gb2312", "auto");
    $mailbody = mb_convert_encoding($mail_content, "gb2312", "auto");
    $mailtype = "HTML";	//"TEXT" OR "HTML"

    $to_list = str_replace(",", ";", $to_list);
    $to_array = explode(';', $to_list);

    //var_dump($to_array);

    foreach($to_array as $addr) {
	$smtpemailto = $addr;
	$smtp = new smtp($smtpserver,$smtpserverport,false,$smtpuser,$smtppass);	//true or false, for auth stmp
	$smtp->debug = false;	// debug information
	$return = ($smtp->sendmail($smtpemailto, $smtpusermail, $mailsubject, $mailbody, $mailtype));
	if ($return == TRUE) {
		echo '**************************************'.'<br />';
		echo '*****发送到'.$smtpemailto.'成功！*****'.'<br />';
		echo '**************************************'.'<br />';
	}
    }
}

else {
    echo "请确认从正常入口进入，并输入完整信息！";
}

?>
</body>
</html>
