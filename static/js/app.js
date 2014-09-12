if(document.location.hostname!="127.0.0.1"){  //Domain switch
        var DOMAIN = "http://rentlisting-snowleo.rhcloud.com";
    }
    else{
        var DOMAIN = "http://127.0.0.1:8000";
    }

var ajaxCall = angular.module('ajaxCall', ['ngResource']); // create AJAX module for REST API

ajaxCall.factory('check_login', ['$resource',
  function($resource){
    return $resource(DOMAIN + '/login/check_login/', {}, {
      query: {method:'GET', params:{}, isArray:true}
    });
  }]);
ajaxCall.factory('get_feature_post', ['$resource',
  function($resource){
    return $resource(DOMAIN + '/polls/get_feature_post/', {}, {
      query: {method:'GET', params:{}, isArray:true}
    });
  }]);
ajaxCall.factory('event', ['$resource',
  function($resource){
    return $resource(DOMAIN + '/polls/event_query/:event_id', {}, {});
  }]);

ajaxCall.factory('Login', ['$http',
  function($http){
    var config={ 
        headers: {
            "X-Requested-With": "XMLHttpRequest",
        },
        xhrFields: {
            withCredentials: true
        },
        data: {
            csrfmiddlewaretoken: '{{ csrf_token }}'
        },
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
            }
        }
    }      
      
    return {
      login: function(data){return $http.post(DOMAIN + '/login/',data,config)},
      check_login: function(){ return $http.get(DOMAIN + '/login/check_login/',config)},
      logout: function(){ return $http.get(DOMAIN + '/login/logout/',config)}
    }
   }
]);

var User= angular.module('User',['ajaxCall']);  // USER module
User.factory('User_info',['Login', function(Login){
    var user=0;
    var update_user= function(data){
        user=data
    }
    var check_login= function(){
        return Login.check_login()
    }
    var login=function(data){
        return Login.login(data);
        //check_login();
    };
    var logout=function(){
        Login.logout();
        user=0;
    };
    return {
        login: login,
        check_login: check_login,
        user:user,
        logout: logout
    };
}]);

var app = angular.module("app", [
    'ngRoute',
    'ajaxCall',
    'User',
    
]);
 app.config(function($httpProvider) { // http request header setting
        $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
        $httpProvider.defaults.headers.post['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
    });

app.controller('ctrl_index', ['$scope','User_info',  // Controller for index page
  function ($scope, User_info) {
      $scope.loading=1;
      $scope.user=0;
      $scope.check_login = function () {
        User_info.check_login().success( function(data){
            $scope.user=data;
            User_info.user=data;
            $scope.loading=0;
            console.log(User_info.user);
        });
      };
      $scope.login_user= function(login_data){        
        User_info.login($.param(login_data)).success(function(data){
                console.log(data);
                $scope.check_login();
                $.fancybox.close();
            }).error(function(data){
                console.log(data);
                $scope.error_msg=data;
            });   
      }
      $scope.logout=function(){
        User_info.logout();
        $scope.user=0;
      }
      
    
  }]);

app.controller('ctrl_login', ['$scope','User_info',  //controller for login page
  function ($scope, User_info) {
    
    $scope.login_user= function(login_data){        
        User_info.login($.param(login_data)).success(function(data){
                console.log(data);
                $.fancybox.close();
            }).error(function(data){
                console.log(data);
                $scope.error_msg=data;
            });   
    }
    //console.log(user_info.user);
  }]);

app.controller('ctrl_main', ['$scope','get_feature_post', // controller for main page
  function ($scope, get_feature_post) {
    $scope.feature_posts =get_feature_post.query();
    console.log($scope.feature_posts);
  }]);

app.controller('ctrl_event', ['$scope','$routeParams','event', // controllor for event page
  function ($scope,$routeParams,event) {
    

    $scope.event =event.get({event_id: $routeParams.id},function(data){
        $scope.loading=0;
        console.log(data.poll);
        $scope.poll=data.poll;
    });
    //console.log($scope.event);
    //console.log($scope.poll);
  }]);

app.config(['$routeProvider',   //router: using different URL for different page and controller
  function($routeProvider) {
    $routeProvider.
      when('/', {
        templateUrl: 'html/main.html',
        controller: 'ctrl_main'
      }).    
      when('/search', {
        templateUrl: 'html/search.html',
        controller: 'ctrl_search'
      }).
      when('/post', {
        templateUrl: 'html/post.html',
        controller: 'ctrl_post'
      }).    
      when('/login', {
        templateUrl: 'html/login.html',
        controller: 'ctrl_login'
      }).   
      when('/event/:id', {
        templateUrl: 'html/event.html',
        controller: 'ctrl_event'
      }).   
      when('/create_account', {
        templateUrl: 'html/create_account.html',
        controller: 'ctrl_create_account'
      }).   
      when('/notice_page', {
        templateUrl: 'html/notice_page.html',
        controller: 'ctrl_notice_page'
      }).   
      when('/conversation_page=:post_id=:asker_id', {
        templateUrl: 'html/conversation_page.html',
        controller: 'ctrl_conversation_page'
      }).   
      otherwise({
        redirectTo: '/'
      });
  }]);        
        
  

