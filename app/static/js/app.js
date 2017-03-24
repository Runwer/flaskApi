(function () {
  'use strict';

  angular.module('MovieApp', ['ngCookies'])
  .controller('MovieController', MovieController)
  .service('MovieDataService',  MovieDataService);

  MovieController.$inject = ['MovieDataService', '$http', '$rootScope', '$cookies'];
  function MovieController(MovieDataService, $http, $rootScope, $cookies) {
    var moviectrl = this;
    // Retrieving a cookie

    MovieDataService.newMovies("2").then(function(d){
      moviectrl.movieOne = d[0];
      $rootScope.movOneDesc = moviectrl.movieOne.Description;
      moviectrl.movieTwo = d[1];
    });
    moviectrl.oldMovieOne = "";
    moviectrl.oldMovieTwo = "";

    this.pickMovie = function (e) {

        moviectrl.picked = e.target.getAttribute('data-value');
        if (moviectrl.picked == "Mov1") {
            var data = {
                win: moviectrl.movieOne.id,
                loose: moviectrl.movieTwo.id
            };
            ga('send', 'event', 'pickMovie', 'picknrOne', 'buttonInteraction');
        } else {
            var data = {
                win: moviectrl.movieTwo.id,
                loose: moviectrl.movieOne.id
            }
            ga('send', 'event', 'pickMovie', 'picknrTwo', 'buttonInteraction');
        }
        moviectrl.user_id = $cookies.get('user_id');
        var req = {
            method: 'POST',
            url: $rootScope.apiuri + 'moviedb/api/v1.0/edge',
            headers : {
                'X-PINGOTHER': 'pingpong',
                'X-USER-ID': moviectrl.user_id
                },
            data: data
            };

        $http(req)
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
            moviectrl.pctMovieOne = d[0];
            moviectrl.pctMovieTwo = d[1]
        });

        MovieDataService.newMovies("2").then(function (d) {
            moviectrl.movieOne = d[0];
            moviectrl.movieTwo = d[1]
        });
    };

    this.changeMovieOne = function (){
      MovieDataService.newMovies("1&vsmovie="+moviectrl.movieTwo.id+"&dump="+moviectrl.movieOne.id).then(function(d){
        moviectrl.movieOne = d[0]
        ga('send', 'event', 'notSeenMovie', 'notSeenOne', 'buttonInteraction');
      });
    };

    this.changeMovieTwo = function (){
      MovieDataService.newMovies("1&vsmovie="+moviectrl.movieOne.id+"&dump="+moviectrl.movieTwo.id).then(function(d){
        moviectrl.movieTwo = d[0]
        ga('send', 'event', 'notSeenMovie', 'notSeenTwo', 'buttonInteraction');
      });
    }


  }
  function MovieDataService ($http, $rootScope, $cookies) {
    var service = this;
    service.user_id = $cookies.get('user_id');
    //setting api URI
    //$rootScope.apiuri = "http://flask-env.3cnseq7p2s.us-west-2.elasticbeanstalk.com/";
    $rootScope.apiuri = "http://127.0.0.1:5000/";
    //List of movies
    var movieout = [];
    $http.defaults.withCredentials = true;

    service.newMovies = function (count){
      var promise = $http({
      method: 'GET',
      withCredentials: true,
      headers: {
        'X-PINGOTHER': 'pingpong',
        'X-USER-ID': service.user_id
      },
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
      //service.user_id = $cookies.getObject('user_id');
      var promise = $http({
      method: 'GET',
      withCredentials: true,
      headers: {
        'X-PINGOTHER': 'pingpong',
        'X-USER-ID': service.user_id
      },
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
