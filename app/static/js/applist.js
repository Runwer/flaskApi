(function () {
  'use strict';

  angular.module('MovieAppList', ['ngRoute'])
  .controller('MovieList', MovieList)
  .service('MovieListService',  MovieListService);

  MovieList.$inject = ['MovieListService', '$rootScope'];
  function MovieList(MovieListService, $rootScope) {
    var movielst = this;
    MovieListService.listMovies().then(function(dat){
      $rootScope.lst = dat
      //console.log($rootScope.lst)
    });

    MovieListService.winPct().then(function(dat){
      $rootScope.winpcts = dat
      //console.log($rootScope.lst)
    });

  }

  function MovieListService ($http, $rootScope) {
    var service = this;
    //$rootScope.apiuri = "http://flask-env.3cnseq7p2s.us-west-2.elasticbeanstalk.com/"
    $rootScope.apiuri = "http://127.0.0.1:5000/"

    //List of movies
    var movieout = [];

    service.listMovies = function (){
      var promise = $http({
      method: 'GET',
      url: $rootScope.apiuri + "moviedb/api/v1.0/toplist"
      }).then(function successCallback(response) {
        return response.data;
      }, function errorCallback(response) {
        // called asynchronously if an error occurs
        // or server returns response with an error status.
        return response
      });
      return promise;
    };

    service.winPct = function (){
      var promise = $http({
      method: 'GET',
      url: $rootScope.apiuri + "moviedb/api/v1.0/winpct"
      }).then(function successCallback(response) {
        return response.data;
      }, function errorCallback(response) {
        // called asynchronously if an error occurs
        // or server returns response with an error status.
        return response
      });
      return promise;
    };

  }
})();
