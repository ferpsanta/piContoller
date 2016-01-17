app.directive('elementInfo', function() { 
  return { 
    restrict: 'EA',
    scope: {
		state: '@',
		site: '@',
		info: '=',
		changeState: '&'
    }, 
    templateUrl: 'js/directives/elementInfo.html' 
  }; 
});