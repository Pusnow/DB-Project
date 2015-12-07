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
        console.log(data.original);
        $scope.original = data.original;

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
            data: {file: file, 'prefix': $scope.task.prefix, 'id' : $scope.original.id}
        }).then(function (resp) {
            $mdToast.show(
          $mdToast.simple()
          .content('원본데이터타입 제출 성공!')
            .hideDelay(3000)
          );
        }, function (resp) {
            console.log('Error status: ' + resp.status);
        }, function (evt) {
            var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
            console.log('progress: ' + progressPercentage + '% ' + evt.config.data.file.name);
        });
    };

    

}]);