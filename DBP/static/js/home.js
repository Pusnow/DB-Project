var app = angular.module('DBPapp', ['ngMaterial','ngFileUpload','md.data.table']);

app.controller('HomeController',['$scope', '$mdSidenav','$http','$mdDialog', function($scope,$mdSidenav,$http,$mdDialog) {

  $scope.toggleSidenav = function(menuId) {
    $mdSidenav(menuId).toggle();
  };

  $scope.login = function(){

  	 	$http.post('/login', {"loginid" : $scope.loginid , "password" : $scope.password}) 
  	 	.success(function(data) { 
			location.reload();
		}) 
		.error(function(err) { 
			$mdDialog.show(
      $mdDialog.alert()
        .parent(angular.element(document.querySelector('#popupContainer')))
        .clickOutsideToClose(true)
        .title('회원정보 오류')
        .textContent('입력한 정보와 일치하는 사용자가 없습니다.')
        .ariaLabel('회원정보 오류')
        .ok('확인')
      );
		})

  };

}]);