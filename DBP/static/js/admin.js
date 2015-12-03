app.controller('AdminController',['$scope', '$mdSidenav','$http', function($scope,$mdSidenav,$http) {

  $scope.toggleSidenav = function(menuId) {
    $mdSidenav(menuId).toggle();
  };


  //init

  $scope.showtasks = function(){
    $http.get('/admin/tasks') 
      .success(function(data) { 
        $scope.menu = 'task';
        console.log(data);
    }) 
    .error(function(err) { 
      console.log(err);
    });

  }

  $scope.showusers = function(){
    $http.get('/admin/users') 
      .success(function(data) { 
        $scope.menu = 'user';
        console.log(data);
    }) 
    .error(function(err) { 
      console.log(err);
    });

  }
  


    

}]);