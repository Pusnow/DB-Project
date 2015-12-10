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
    "birth" : new Date("1994-01-01"),
    "cellphone" : ""
    }

  }


  $scope.newuser = function(){

    var data = $scope.user;
    data.birth = $scope.user.birth.toDateString();
    $http.post('/admin/newuser', data) 
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


    $scope.showusers = function(){
    $http.get('/admin/users') 
      .success(function(data) { 
        $scope.menu = 'users';
        var userlist = data.users;
        console.log(data);    
        for (var i in userlist){
          userlist[i].birth = new Date(userlist[i].birthstring );
          userlist[i].age = parseInt((new Date() - new Date(userlist[i].birthstring ) )/(60*60*24*365*1000*10)) + "0대";
          console.log(userlist[i].age );
        } 
        $scope.userlist = userlist;
    }) 
    .error(function(err) { 
      console.log(err);
    });

  }

  $scope.showuser = function(id){
    $http.post('/admin/user', {"id" : id}) 
      .success(function(data) { 
        var user  = data.user;
        user.birth = new Date(user.birthstring );
        $scope.user = user
    }) 
    .error(function(err) { 
      console.log(err);
    });

  }

  $scope.edituser = function (){
  var data = $scope.user;
  data.birth = $scope.user.birth.toDateString();
  $http.post('/admin/useredit',data) 
      .success(function(data) { 
         if (data.code == "success"){
          $scope.showuser($scope.user.id);
        $mdToast.show(
          $mdToast.simple()
          .content('사용자 정보 수정 성공!')
            .hideDelay(3000)
        );
      }
    }) 
    .error(function(err) { 
      console.log(err);
    });


}



  $scope.newSch = function(chip) {

    var info = chip.split(":")
    var name = info[0];
    var type = "str"
    if (info.length > 1){
      if (info[1] == "int"){
        type = "int";
      }
      if (info[1] == "datetime"){
        type = "datetime";
      }
    }

      return {
        name: name,
        type: type
      };
    };
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

  $scope.selectedIndex  = 0;
  $scope.showtask = function(prefix){
    $scope.selectedIndex = 0;
    $http.post('/admin/task',{"prefix" : prefix}) 
      .success(function(data) { 
        $scope.task = data.task;
        
        initoriginalform();

    }) 
    .error(function(err) { 
      console.log(err);
    });

  }

  $scope.taskstatus = function(prefix, status){
    $scope.selectedIndex = 0;
    $http.post('/admin/taskstatus',{"prefix" : prefix, "status" : status}) 
      .success(function(data) { 
        if (data.code == "success"){
         $mdToast.show(
          $mdToast.simple()
          .content('태스크 상태 변경 성공')
            .hideDelay(3000)
          );
         $scope.task = data.task;
          initoriginalform();
         }
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
  $scope.showtupples = function(){
    $http.post('/admin/showtupples', $scope.task) 
      .success(function(data) { 
        if (data.code == "success"){
          $scope.tpquery = {
          order: 'id',
          limit: 10,
          page: 1
        };

        console.log(data);
          $scope.tupples = data;



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


  $scope.showuserparseds = function (userid) {
    $http.post('/admin/userparsds',{"id" : userid}).success(function(data){
      $scope.psquery = {
          order: 'id',
          limit: 10,
          page: 1
        };
      $scope.parsedlist = data.parsedlist
  })
}

  



  


    

}]);