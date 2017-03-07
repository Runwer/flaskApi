(function () {
  'use strict';

  angular.module('MovieApp', ['ngCookies'])
  .controller('MovieController', MovieController)
  .service('MovieDataService',  MovieDataService);

  MovieController.$inject = ['MovieDataService', '$http', '$rootScope', '$cookies'];
  function MovieController(MovieDataService, $http, $rootScope, $cookies) {
    var moviectrl = this;
    // Retrieving a cookie
    moviectrl.userID = $cookies.getObject('uid');
    // needs to be rewritten for actual cookiesetting - Setting cookie
    if (typeof moviectrl.userID !== 'undefined') {
      $rootScope.greeting = "Welcome Back" + moviectrl.userID;
    }
    else{
      $rootScope.greeting = "Its your first time and we are stoked to meet you.";
      $cookies.putObject('uid', '5', {expires: new Date(3017,6, 30)});
    }


    MovieDataService.newMovies("2").then(function(d){
      moviectrl.movieOne = d[0]
      $rootScope.movOneDesc = moviectrl.movieOne.Description
      moviectrl.movieTwo = d[1]
    });
    moviectrl.oldMovieOne = ""
    moviectrl.oldMovieTwo = ""


    this.pickMovie = function (e) {
        moviectrl.picked = e.target.getAttribute('data-value');
        if (moviectrl.picked == "Mov1") {
            var data = {
                user: moviectrl.userID,
                win: moviectrl.movieOne.id,
                loose: moviectrl.movieTwo.id
            };
        } else {
            var data = {
                user: moviectrl.userID,
                win: moviectrl.movieTwo.id,
                loose: moviectrl.movieOne.id
            };
        }
        ;

        $http.post($rootScope.apiuri + 'moviedb/api/v1.0/edge', data)
            .then(function (data, status, headers) {
                //console.log(data);
            }, function errorCallback(response) {
                // called asynchronously if an error occurs
                // or server returns response with an error status.
                return response;
            })
        ;

        moviectrl.oldMovieOne = moviectrl.movieOne;
        moviectrl.oldMovieTwo = moviectrl.movieTwo;
        MovieDataService.pctMovies(moviectrl.movieOne.id, moviectrl.movieTwo.id).then(function (d) {
            moviectrl.pctMovieOne = d[0]
            moviectrl.pctMovieTwo = d[1]
        });

        MovieDataService.newMovies("2").then(function (d) {
            moviectrl.movieOne = d[0]
            moviectrl.movieTwo = d[1]
        });
    }

    this.changeMovieOne = function (){
      MovieDataService.newMovies("1&vsmovie="+moviectrl.movieTwo.id+"&dump="+moviectrl.movieOne.id).then(function(d){
        moviectrl.movieOne = d[0]
      });
    }

    this.changeMovieTwo = function (){
      MovieDataService.newMovies("1&vsmovie="+moviectrl.movieOne.id+"&dump="+moviectrl.movieTwo.id).then(function(d){
        moviectrl.movieTwo = d[0]
      });
    }


  };
  function MovieDataService ($http, $rootScope) {
    var service = this;
    //setting api URI
    $rootScope.apiuri = "http://flask-env.3cnseq7p2s.us-west-2.elasticbeanstalk.com/"
    //$rootScope.apiuri = "http://127.0.0.1:5000/"
    //List of movies
    var movieout = [];

    service.newMovies = function (count){
      var promise = $http({
      method: 'GET',
      url: $rootScope.apiuri+"moviedb/api/v1.0/movies?count="+count
      }).then(function successCallback(response) {
        return response.data; //Probably need to remove movies
      }, function errorCallback(response) {
        // called asynchronously if an error occurs
        // or server returns response with an error status.
        return response
      });
      return promise;
    };

    service.pctMovies = function (id1, id2){
      var promise = $http({
      method: 'GET',
      url: $rootScope.apiuri+"moviedb/api/v1.0/moviepct?mov1="+id1+"&mov2="+id2
      }).then(function successCallback(response) {
        return response.data; //Probably need to remove movies
      }, function errorCallback(response) {
        // called asynchronously if an error occurs
        // or server returns response with an error status.
        return response
      });
      return promise;
    };

    service.oldMovies = function () {
      return "movie"
    }
  }

})();
