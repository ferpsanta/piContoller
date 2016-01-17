<?php
if (!isset($_GET['action']) || !isset($_GET['mod'])) {
    header('400 Bad Request');
    exit;
}

try {
    $module       = $_GET['mod'];
	$action		  = $_GET['action'];
	
    switch ($module) {
	  case "gpioManager":
	    require_once "controllers/GPIO_controller.php";
		
		$GPIO_controller = new GPIOController;
		$result = $GPIO_controller->execute($action);
	    break;
	  case "dbManager":
	    #TODO
		break;
	  default:
		header('400 Bad Request');
		exit;
	}
	
    echo json_encode($result);
	
} catch(Exception $e) {
    header('404 Not Found');
    exit;
}
?>