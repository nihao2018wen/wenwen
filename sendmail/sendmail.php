<?php 
/**
* 邮件发送函数
*/
function sendMail($to, $title, $content) {
	$config = array(
		'SMTP_HOST' => 'smtp.qq.com', //SMTP服务器
		'SMTP_PORT' => '465', //SMTP服务器端口
		'SMTP_USER' => 'xxxxxx@qq.com', //SMTP服务器用户名
		'SMTP_PASS' => 'xxxxxx', //SMTP服务器密码 
		'FROM_EMAIL' => 'xxxxxx@qq.com',
		'FROM_NAME' => '张三', //发件人名称
		'SESSION_EXPIRE'=>'72',
	);
	Vendor('PHPMailer.PHPMailerAutoload');     
	$mail = new \PHPMailer(); //实例化
	// 是否启用smtp的debug进行调试 开发环境建议开启 生产环境注释掉即可 默认关闭debug调试模式，
    // 可选择的值有 1 、 2 、 3
    // $mail->SMTPDebug = 2;     

    //使用smtp鉴权方式发送邮件
    $mail->isSMTP();                                      
    //smtp需要鉴权 这个必须是true
    $mail->SMTPAuth = true;                               
    // qq 邮箱的 smtp服务器地址，这里当然也可以写其他的 smtp服务器地址
    $mail->Host = 'smtp.qq.com';
    //smtp登录的账号 这里填入字符串格式的qq号即可
    $mail->Username = $config['SMTP_USER'];                 
    // 这个就是之前得到的授权码，一共16位,在qq邮箱 账号设置里边设置
    $mail->Password = $config['SMTP_PASS'];     
    //设置使用ssl加密方式登录鉴权                      
    $mail->SMTPSecure = 'ssl';                            
    // //设置ssl连接smtp服务器的远程服务器端口号，可选465或587
    $mail->Port = $config['SMTP_PORT'];

    //设置smtp的helo消息头 这个可有可无 内容任意
    // $mail->Helo = 'Hello smtp.qq.com Server';

    //设置发送的邮件的编码 也可选 GB2312
    $mail->CharSet = 'UTF-8';                        

    $mail->setFrom($config['FROM_EMAIL'], $config['FROM_NAME']);
    // $to 为收件人的邮箱地址，如果想一次性发送向多个邮箱地址，则只需要将下面这个方法多次调用即可
	foreach($to as $v){
		$mail->addAddress($v);
	}
    //邮件正文是否为html编码 注意此处是一个方法 不再是属性 true或false
    $mail->isHTML(true);
    // 该邮件的主题
    $mail->Subject = $title;
    // 该邮件的正文内容
    $mail->Body = $content;
	
    // 使用 send() 方法发送邮件
    if(!$mail->send()) {
      return 'Mailer Error: ' . $mail->ErrorInfo;
    } else {
      return "Message has been sent";
    }
}
?>