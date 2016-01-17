app.controller('MainController', ['$scope', '$timeout', 'gpioManager',
 function($scope, $timeout, gpioManager) {
	
	//TODO: Get language fron DB
	$scope.tittle = 'piController';
	$scope.home = 'Home';
	$scope.logs = 'Logs';
	$scope.stats = 'Estadisticas';
	$scope.elementState = 'Estado';
	$scope.elementSite = 'Lugar';
	
	$scope.elements =
	[
		{
			name: 		'Caldera',
			site: 		'Habitacion 3',
			type: 		'Relay',
			state:  	'OFF',
			icon:		'img/heater_OFF.png'
		}
	];
	
	$scope.changeState = function () {
		gpioManager.setStatus($scope.elements[0].state).then(
			$scope.checkState()
		)
	}
	
	$scope.checkState = function () {
		gpioManager.getStatus().then( 
			function(polledState) {
				if(polledState == 0) {
				  $scope.elements[0].state = 'OFF';
				  $scope.elements[0].icon = 'img/heater_OFF.png';
				} else {
				  $scope.elements[0].state = 'ON';
				  $scope.elements[0].icon = 'img/heater_ON.png';
				}
			}
		)
	}
	
	//TODO: Scale to multiple elements
	$scope.passiveCheck = function () {
		$scope.checkState();
		$timeout($scope.passiveCheck, 5000);
	};
	
	
	
	
}]);