app.controller('EvaluatorContoller',['$scope', '$mdSidenav','$http', '$mdDialog', '$mdToast','Upload', function($scope,$mdSidenav,$http,$mdDialog,$mdToast,Upload) {
  $scope.originalid = null;
  $scope.task = {
    "name" : "",
    "prefix" : "",
    "duration" : "",
    "information" : "",
    "schemas" : []
  }
  $scope.menu = 'home';
  $scope.toggleSidenav = function(menuId) {
    $mdSidenav(menuId).toggle();
  };

  $scope.logout = function(){
    $http.post('/logout').success(function(){location.reload();});
  }


  $scope.showevaluate = function(){
    $http.get('/evaluator/parseds').success(function(data){
      $scope.menu ="evaluate"
      $scope.parsedlist = data.parsedlist
      console.log($scope.parsedlist)


    });
  }

  $scope.showparsed = function(prefix,id){
    $http.post('/evaluator/parsed',{"prefix" : prefix, "id" : id}).success(function(data){
      $scope.parsed = data.parsed;
      $scope.task = data.task;
      $scope.eval = {
        "score" : 0,
        "pass" : false,
        "prefix" : data.task.prefix,
        "id" : data.parsed.id
      }
    });
  }

  $scope.submitevaluate = function(){
    console.log($scope.eval)
      $http.post('/evaluator/submitevaluate',$scope.eval).success(function(data){

      if (data.code == "success"){
        $scope.parsed = {};
        $scope.task = {};
        $scope.showevaluate();
        $mdToast.show(
          $mdToast.simple()
          .content('평가 제출 성공!')
            .hideDelay(3000)
        );

      }


    });

  }



}]);


