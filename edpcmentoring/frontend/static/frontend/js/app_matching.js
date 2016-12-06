//
//
// We require that the app is loaded first 
// 
//

app.controller("MatchFormCtrl", ['$scope', 'ngDialog', '$http', 'MatchingService', '$rootScope', function ($scope,ngDialog,$http,MatchingService,$rootScope){
        $scope.me ={}

	$scope.searching=[]
        $scope.searching_rels={} // Members searching for partners
        $scope.rels=""

        $scope.getSearchingRels = function(){
		MatchingService.getSeeking().then(function(response){
			$scope.searching = response
			$scope.searching_rels.mentors = response.filter($scope.filterSearchingMentor)
			$scope.searching_rels.mentees = response.filter($scope.filterSearchingMentee)
		})
	}

        $scope.filterSearchingMentor = function(member){
		//Mentors that are searching / available
		console.log("searching: "+JSON.stringify(member))
		return member.is_seeking_mentee
	}

        $scope.filterSearchingMentee = function(member){
		//Mentees that are searching / available
		console.log("searching: "+JSON.stringify(member))
		return member.is_seeking_mentor 
	}

        $rootScope.$watch('rels',function(){
		//on rels chnage update our lists
		$scope.getSearchingRels()
        })

	$scope.getSearchingRels()
        
        $scope.matchMentee = function(mentee){
		$scope.mentee = mentee
		ngDialog.open({
		    	scope: $scope,
			template: 'match-mentee',
			controller: 'MatchMenteeCtrl'
		})

		//alert("match user: "+JSON.stringify(user))
	}
}])



app.controller("MatchMenteeCtrl",['$scope', '$rootScope', 'ngDialog', 'MatchingService', function($scope,$rootScope,ngDialog,MatchingService){
        $scope.match = function(mentor){
		// $scope.user is the mentee!
		myrel={mentor:mentor, mentee:$scope.user}
		MatchingService.addRel(myrel).then(function(response){
			$rootScope.rels = new Date() //triggers watch
			ngDialog.close()
		},function(error){
			console.log("FIXME: problems removing mentee")
		})

	}

	$scope.close = function(){
		ngDialog.close()
	}
}])


app.service('MatchingService', ['$http','$q',function($http, $q) {
  return {
    'getSeeking': function() { //list those seeking a mentee
      var defer = $q.defer();
      $http.get("/api/mm/seekrel/").success(function(resp){
	defer.resolve(resp);
      }).error( function(err) {
        defer.reject(err);
      });
      return defer.promise;
    },
  }
}])
