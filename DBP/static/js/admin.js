app.controller('AdminController',['$scope', '$mdSidenav','$http', '$mdDialog', '$mdToast', function($scope,$mdSidenav,$http,$mdDialog,$mdToast) {

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

  $scope.shownewtask = function(){
    $scope.menu = 'newtask';
    $scope.task = {
    "name" : "",
    "prefix" : "",
    "duration" : "",
    "information" : "",
    "schemas" : []
    }

  }
  $scope.shownewuser = function(){
    $scope.menu = 'newuser';
    $scope.user = {
    "loginid" : "",
    "password" : "",
    "name" : "",
    "gender" : "",
    "address" : "",
    "role" : "",
    "birth" : Date(),
    "cellphone" : ""
    }

  }
  $scope.newuser = function(){

    var data = $scope.user;
    data.birth = data.birth.toUTCString();
    $http.post('/admin/newuser', $scope.user) 
      .success(function(data) { 
      if (data.code == "success"){
         $scope.user = {
          "loginid" : "",
          "password" : "",
          "name" : "",
          "gender" : "",
          "address" : "",
          "role" : "",
          "birth" : Date(),
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

  $scope.showusers = function(){
    $scope.menu = 'users';
    $scope.user = {
    "loginid" : "",
    "password" : "",
    "name" : "",
    "gender" : "",
    "address" : "",
    "role" : "",
    "birth" : Date(),
    "cellphone" : ""
    }

  }

  $scope.submitTaskForm = function(){
    $http.post('/admin/newtask', $scope.task) 
      .success(function(data) { 
      if (data.code == "success"){
        $scope.task = {
          "name" : "",
          "prefix" : "",
          "duration" : "",
          "information" : "",
          "schemas" : []
        }
        $mdToast.show(
          $mdToast.simple()
          .content('태스크 생성 성공!')
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
   $scope.resetTaskForm = function(){
     $scope.task = {
      "name" : "",
      "prefix" : "",
      "duration" : "",
      "information" : "",
      "schemas" : []
    }
  }  

  $scope.showtasks = function(){
    $http.get('/admin/tasks') 
      .success(function(data) { 
        $scope.menu = 'task';
        $scope.tasklist = data.tasks;
    }) 
    .error(function(err) { 
      console.log(err);
    });

  }

  $scope.showtask = function(prefix){
    $http.post('/admin/task',{"prefix" : prefix}) 
      .success(function(data) { 
        $scope.task = data.task;
        initoriginalform();

    }) 
    .error(function(err) { 
      console.log(err);
    });

  }

  function initoriginalform(){
     $scope.original = {
      "prefix" : $scope.task.prefix,
      "name" : "",
      "length" : 0,
      "schemas": []
    }
    for (var i in $scope.task.schemas) {
      $scope.original.schemas.push({ "label":$scope.task.schemas[i], "col" : 0});
    }
  }

  $scope.showneworiginal = function(){
    initoriginalform();

  }

  $scope.submitNewOriginal = function(){
    $http.post('/admin/neworiginal', $scope.original) 
      .success(function(data) { 
        if (data.code == "success"){
         $mdToast.show(
          $mdToast.simple()
          .content('원본 데이터 타입 생성 성공!')
            .hideDelay(3000)
          );
          initoriginalform();
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
        console.log(err);
      });
  }
  function initoriginals(){
    $http.post('/admin/showoriginals', $scope.task) 
      .success(function(data) { 
        if (data.code == "success"){
          console.log(data);
          $scope.originallist = data.originallist;
          
         }
          else if (data.code == "err"){
           
          }
      }) 
      .error(function(err) { 
        console.log(err);
      });
  }
  $scope.showoriginals = function(){
    initoriginals();
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