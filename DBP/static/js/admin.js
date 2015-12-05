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
    "birth" : new Date(),
    "cellphone" : ""
    }

  }


  $scope.newuser = function(){

    var data = $scope.user;
    data.birth = $scope.user.birth.toUTCString();
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
          "birth" : new Date(),
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
    $http.get('/admin/users') 
      .success(function(data) { 
        $scope.menu = 'users';
        $scope.userlist = data.users
    }) 
    .error(function(err) { 
      console.log(err);
    });

  }

  $scope.showuser = function(id){
    $http.post('/admin/user', {"id" : id}) 
      .success(function(data) { 
        $scope.user = data.user
    }) 
    .error(function(err) { 
      console.log(err);
    });

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
  $scope.changestatus = function(id,status){
    $http.post('/admin/changesubmitterstatus',{"prefix" : $scope.task.prefix , "id" :id , "status" : status}) 
      .success(function(data) { 
        if (data.code == "success"){
         $mdToast.show(
          $mdToast.simple()
          .content('제출자 상태 변경 성공')
            .hideDelay(3000)
          );
          initoriginalform();
         }

    }) 
    .error(function(err) { 
      console.log(err);
    });

  }

  $scope.showsubmitters = function(prefix){
    $http.post('/admin/submitters',{"prefix" : prefix}) 
      .success(function(data) { 
        $scope.sbquery = {
          order: 'id',
          limit: 10,
          page: 1
        };

        $scope.submitters = data.submitters;
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
          $scope.orquery = {
          order: 'id',
          limit: 10,
          page: 1
        };
          $scope.originallist = data.originallist;
          
         }
          else if (data.code == "err"){
           
          }
      }) 
      .error(function(err) { 
        console.log(err);
      });
  }
  $scope.showparseds = function(){
    $http.post('/admin/showparseds', $scope.task) 
      .success(function(data) { 
        if (data.code == "success"){
          $scope.psquery = {
          order: 'id',
          limit: 10,
          page: 1
        };
          $scope.parsedlist = data.parsedlist;
          
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


  $scope.logout = function(){
    $http.post('/logout').success(function(){location.reload();});
  }



  


    

}]);