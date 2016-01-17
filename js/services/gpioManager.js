app.factory('gpioManager', ['$http', function($http) { 
  return {
	  getStatus: function () {
					return $http.get('php/ajax_handler.php?mod=gpioManager&action=getStatus')
								.then(function(result) {
									return angular.fromJson(result.data);
								});
				},
	  setStatus: function (state) {
					if(state == 'OFF') {
						action = 'turnON';
					}else {
						action = 'turnOFF';
					}
					return $http.get('php/ajax_handler.php?mod=gpioManager&action='+action)
								.then(function(result) {
									return angular.fromJson(result.data);
								});
				}
  };
}]);