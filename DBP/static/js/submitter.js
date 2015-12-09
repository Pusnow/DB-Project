app.controller('SubmitterContoller',['$scope', '$mdSidenav','$http', '$mdDialog', '$mdToast','Upload', function($scope,$mdSidenav,$http,$mdDialog,$mdToast,Upload) {
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

  $scope.showapply = function(){

     $http.get('/submitter/tasks') 
      .success(function(data) { 
        $scope.menu = 'apply';
        $scope.tasklist = data.tasks;
    }) 
    .error(function(err) { 
      console.log(err);
    });
  }

   $scope.showsubmit = function(){

     $http.get('/submitter/submit') 
      .success(function(data) { 
        $scope.menu = 'submit';
        $scope.tasklist = data.tasks;
    }) 
    .error(function(err) { 
      console.log(err);
    });
  }
  




  $scope.showtask = function(prefix){
    $http.post('/submitter/task',{"prefix" : prefix}) 
      .success(function(data) { 
        console.log(data.task);
        $scope.task = data.task;

    }) 
    .error(function(err) { 
      console.log(err);
    });

  }



  $scope.applytask = function(){
    $http.post('/submitter/applytask',{"prefix" : $scope.task.prefix}) 
      .success(function(data) { 
        if (data.code == "success"){
         $mdToast.show(
          $mdToast.simple()
          .content('태스크 지원 성공!')
            .hideDelay(3000)
          );
          $scope.task = data.task;
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
  $scope.showoriginal = function(id){
    $http.post('/submitter/original',{"id" : id, "prefix" : $scope.task.prefix}) 
      .success(function(data) { 
        $scope.original = data.original;
        $scope.original.duration_start  = new Date();
        $scope.original.duration_end  = new Date();

    }) 
    .error(function(err) { 
      console.log(err);
    });

  }
  

  $scope.showparsed = function(){
    $http.post('/submitter/parsed',{"prefix" : $scope.task.prefix}) 
      .success(function(data) { 
        console.log(data);
        $scope.psquery = {
          order: 'original',
          limit: 5,
          page: 1
        };
        $scope.parsedlist = data.parsedlist;

    }) 
    .error(function(err) { 
      console.log(err);
    });

  }

  $scope.submitoriginal = function(file){

        Upload.upload({
            url: '/submitter/submitoriginal',
            data: {file: file, 'prefix': $scope.task.prefix, 'id' : $scope.original.id, "duration_start" : $scope.original.duration_start.toDateString(),  "duration_end" : $scope.original.duration_end.toDateString()}
        }).then(function (resp) {
          console.log(resp)
          if (resp.data.code == "success"){
            $scope.showoriginal($scope.original.id)
              $mdToast.show(
            $mdToast.simple()
            .content('원본데이터타입 제출 성공!')
              .hideDelay(3000)
            );
            }
            else {
              $mdDialog.show(
          $mdDialog.alert()
            .parent(angular.element(document.querySelector('#popupContainer')))
            .clickOutsideToClose(true)
            .title('오류')
            .textContent("지원하지 않는 파일입니다.")
            .ariaLabel('오류')
            .ok('확인')
          );
         }
            
        }, function (resp) {
            console.log('Error status: ' + resp.status);
        }, function (evt) {
            var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
            console.log('progress: ' + progressPercentage + '% ' + evt.config.data.file.name);
        });
    };

$scope.showstatistics = function(){
   $scope.menu = "statistics";

   

   $http.get('/submitter/statistics') 
      .success(function(data) { 
        $scope.menu = "statistics";
        console.log(data);
        var user  = data.user;
        user.birth = new Date(user.birthstring );
        $scope.user = user;
    }) 
    .error(function(err) { 
      console.log(err);
    });


}


$scope.showedituser = function (){
  
  $http.get('/user/info') 
      .success(function(data) { 
        $scope.menu = "edituser";
        var user  = data.user;
        user.birth = new Date(user.birthstring );
        $scope.user = user;
    }) 
    .error(function(err) { 
      console.log(err);
    });


}

    
$scope.edituser = function (){
  var data = $scope.user;
  data.birth = $scope.user.birth.toDateString();
  $http.post('/user/edit',data) 
      .success(function(data) { 
         if (data.code == "success"){
          $scope.showedituser();
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

$scope.showdeleteuser = function(){
   $scope.menu = "deleteuser";


}

$scope.deleteuser =  function(){
    $http.post('/user/delete').success(function(){location.reload();});
  }


}]);