<?php

include_once('interfaces/controller.php');

class GPIOController implements Controller
{
    public function execute($input)
    {
        switch ($input) {
			case "turnON":
			  $txSocket = socket_create (AF_UNIX, SOCK_DGRAM, 0);
			  if (socket_connect($txSocket, "/tmp/serverRx_socket")) {
				 if (socket_write($txSocket, "ON")) {
					$result = "Success";
				 } 
			  }
			  socket_close ($txSocket);
			break;
		  case "turnOFF":
			  $txSocket = socket_create (AF_UNIX, SOCK_DGRAM, 0);
			  if (socket_connect($txSocket, "/tmp/serverRx_socket")) {
				 if (socket_write($txSocket, "OFF")) {
					$result = "Success";
				 } 
			  }
			  socket_close ($txSocket);
			break;
		  case "getStatus":
			  $txSocket = socket_create (AF_UNIX, SOCK_DGRAM, 0);
			  $rxSocket = socket_create (AF_UNIX, SOCK_DGRAM, 0);
			  if( socket_bind($rxSocket, "/tmp/clientRx_socket") ) {
			    if (socket_connect($txSocket, "/tmp/serverRx_socket")) {
				  if (socket_write($txSocket, "STATUS")) {
					$datagram = socket_read($rxSocket, 1024);
					$result = $datagram;
				  } 
			    }
			  }
			  socket_close ($txSocket);
			  socket_close ($rxSocket);
			  unlink("/tmp/clientRx_socket");
			break;
		  default:
			header('400 Bad Request');
			exit;
		}
		
        return $result;
    }
}
?>