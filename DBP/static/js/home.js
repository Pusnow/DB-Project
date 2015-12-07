var app = angular.module('DBPapp', ['ngMaterial','ngFileUpload','md.data.table']);

app.controller('HomeController',['$scope', '$mdSidenav','$http','$mdDialog', '$mdToast', function($scope,$mdSidenav,$http,$mdDialog, $mdToast) {
  $scope.menu = "home";
  $scope.toggleSidenav = function(menuId) {
    $mdSidenav(menuId).toggle();
  };

  $scope.showlogin = function (){
    $scope.menu ="login";
  }
  $scope.showhome = function (){
    $scope.menu ="home";
  }
  $scope.showjoin = function (){
    $scope.menu ="join";
    $scope.user = {
    "loginid" : "",
    "password" : "",
    "name" : "",
    "gender" : "",
    "address" : "",
    "role" : "",
    "birth" : new Date("1994-01-01"),
    "cellphone" : ""
    }

  }
  


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

  $scope.join = function(){
    var data = $scope.user;
    data.birth = $scope.user.birth.toDateString();
    $http.post('/user/join', data) 
      .success(function(data) { 
      if (data.code == "success"){
         $scope.user = {
          "loginid" : "",
          "password" : "",
          "name" : "",
          "gender" : "",
          "address" : "",
          "role" : "",
          "birth" : new Date("1994-01-01"),
          "cellphone" : ""
          }
        $mdToast.show(
          $mdToast.simple()
          .content('사용자 생성 성공!')
            .hideDelay(3000)
        );
      }
      else if (data.code == "err"){
        $mdDialog.show(
          $mdDialog.alert()
            .parent(angular.element(document.querySelector('#popupContainer')))
            .clickOutsideToClose(true)
            .title('오류')
            .textContent(data.msg)
            .ariaLabel('오류')
            .ok('확인')
          );
      }
    }) 
    .error(function(err) { 
      $mdDialog.show(
      $mdDialog.alert()
        .parent(angular.element(document.querySelector('#popupContainer')))
        .clickOutsideToClose(true)
        .title('오류')
        .textContent("알 수 없는 오류")
        .ariaLabel('오류')
        .ok('확인')
      );
    })




  }

}]);