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
	// Filter for full list
        $scope.filterSearchingMentor = function(member){
		//Mentors that are searching / available
		return member.is_seeking_mentee
	}

        $scope.filterSearchingMentee = function(member){
		//Mentees that are searching / available
		return member.is_seeking_mentor 
	}

 	// Filters for matching modals
        $scope.removeCurrentMentors = function(){
		//from the $scope.searching_rels.mentors array 
                //remove any members who are active mentors for the current mentee
		
	}

        $rootScope.$watch('rels',function(){
		//on rels chnage update our lists
		$scope.getSearchingRels()
        })

	$scope.getSearchingRels()
         
        $scope.matchMentor = function(mentor){
		$scope.mentor = mentor
		$scope.skip_invite=0;

		ngDialog.open({
		    	scope: $scope,
			template: 'match-mentor',
			controller: 'MatchMentorCtrl'
		})

	}
     
        $scope.matchMentee = function(mentee){
		$scope.mentee = mentee
		$scope.skip_invite=0;

		ngDialog.open({
		    	scope: $scope,
			template: 'match-mentee',
			controller: 'MatchMenteeCtrl'
		})

	}
}])



app.controller("MatchMentorCtrl",['$scope', '$rootScope', 'ngDialog', 'MatchingService', function($scope,$rootScope,ngDialog,MatchingService){

	// The list of available Mentors needs to be filtered 
	// remove members who have been matched already to this user
	$scope.mentors_mentees = $scope.mentor.user.mentor_relationships.reduce(function(a,b){return a.concat(b.mentee.id) },[$scope.mentor.user.id])
	//we could also setup the filtered array here too?
	$scope.available_mentees = function (){
		return $scope.searching_rels.mentees.filter(function(mentor){
			return $scope.mentees_mentees.indexOf(mentor.user.id) == -1;
		});
	}; 

        $scope.set_seeker = function(seeker){
                $scope.selected_seeker = seeker;
        }


        $scope.match = function(mentee){
		// $scope.user is the mentee!
		myrel={mentor:mentee, mentor:$scope.user}
		MatchingService.addRel(myrel).then(function(response){
			$rootScope.rels = new Date() //triggers watch
			ngDialog.close()
		},function(error){
			console.log("FIXME: problems removing mentee")
		})

	}

        $scope.actionInvite = function(inv){
		// I am a match maker and I wish for both parties to accept the invitation
		// to do this I create a new invite to replace this and any other invite associted to the relationship
		// and set accept by both parties
		inv = {id:inv.id,mentor_response:'A',mentee_response:'A'}
		inv.mentee_response='A' 
		inv.mentor_response='A' 
		MatchingService.updateInv(inv).then(function(response){
                        $rootScope.rels = new Date() //triggers watch
                        ngDialog.close()
                },function(error){
                        console.log("FIXME: problems removing mentee")

		})
	}

        $scope.declineInvite = function(inv){
		// I am a match maker and I wish for both parties to accept the invitation
		// to do this I create a new invite to replace this and any other invite associted to the relationship
		// and set accept by both parties
		//inv = {id:inv.id,mentor_response:'D',mentee_response:'D'}
		inv.mentee_response='D' 
		inv.mentor_response='D' 
		MatchingService.updateInv(inv).then(function(response){
                        $rootScope.rels = new Date() //triggers watch
                        ngDialog.close()
                },function(error){
                        console.log("FIXME: problems removing mentee")

		})
	}

	$scope.addMentee = function(mentee){
		MatchingService.addMentee(
			{mentee:mentee,mentor:$scope.mentor.user,mentor_response:'A',mentee_response:'A'}
		).then(function(response){
        	        $rootScope.rels = new Date() //triggers watch
                	ngDialog.close()
                },function(error){
                       	console.log("FIXME: problems adding mentor")
		})	
	}

	$scope.close = function(){
		ngDialog.close()
	}
}])




app.controller("MatchMenteeCtrl",['$scope', '$rootScope', 'ngDialog', 'MatchingService', function($scope,$rootScope,ngDialog,MatchingService){

	// The list of available Mentors needs to be filtered 
	// remove members who have been matched already to this user
	console.log($scope.mentee)
	$scope.mentees_mentors = $scope.mentee.user.mentee_relationships.reduce(function(a,b){return a.concat(b.mentor.id) },[$scope.mentee.user.id])
	//we could also setup the filtered array here too?
	$scope.available_mentors = function (){
		return $scope.searching_rels.mentors.filter(function(mentor){
			return $scope.mentees_mentors.indexOf(mentor.user.id) == -1;
		});
	}; 
	// $scope.mentors = $scope.searching_rels.mentors.filter($scope.filterCurrentMentors)

        $scope.set_seeker = function(seeker){
                console.log("setting seeker")
                $scope.selected_seeker = seeker;
        }


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

        $scope.actionInvite = function(inv){
		// I am a match maker and I wish for both parties to accept the invitation
		// to do this I create a new invite to replace this and any other invite associted to the relationship
		// and set accept by both parties
		//inv = {id:inv.id,mentor_response:'A',mentee_response:'A'}
		inv.mentee_response='A' 
		inv.mentee_response='D' 
		MatchingService.updateInv(inv).then(function(response){
                        $rootScope.rels = new Date() //triggers watch
                        ngDialog.close()
                },function(error){
                        console.log("FIXME: problems removing mentee")

		})
	}

        $scope.declineInvite = function(inv){
		// I am a match maker and I wish for both parties to accept the invitation
		// to do this I create a new invite to replace this and any other invite associted to the relationship
		// and set accept by both parties
		//inv = {id:inv.id,mentor_response:'D',mentee_response:'D'}
		inv.mentee_response='D' 
		inv.mentor_response='D' 
		MatchingService.updateInv(inv).then(function(response){
                        $rootScope.rels = new Date() //triggers watch
                        ngDialog.close()
                },function(error){
                        console.log("FIXME: problems removing mentee")

		})
	}

	$scope.addMentor = function(mentor){
		MatchingService.addMentor(
			{mentor:mentor,mentee:$scope.mentee.user,mentee_response:'A',mentor_response:'A'}
		).then(function(response){
        	        $rootScope.rels = new Date() //triggers watch
                	ngDialog.close()
                },function(error){
                       	console.log("FIXME: problems adding mentor")
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
    'updateInv': function(inv) { //done via saving an accepted invite
      var defer = $q.defer();
      $http.patch("/api/mm/invitations/"+inv.id+"/",inv).success(function(resp){
        defer.resolve(resp);
      }).error( function(err) {
        defer.reject(err);
      });
      return defer.promise;
    },
    'addMentor': function(inv) { //done via adding completed invite - associated to current user
      var defer = $q.defer();
      $http.post("/api/mm/invitations/",inv).success(function(resp){
        defer.resolve(resp);
      }).error( function(err) {
        defer.reject(err);
      });
      return defer.promise;
    },
    'addMentee': function(inv) { //done via adding completed invite - associated to current user
      var defer = $q.defer();
      $http.post("/api/mm/invitations/",inv).success(function(resp){
        defer.resolve(resp);
      }).error( function(err) {
        defer.reject(err);
      });
      return defer.promise;
    },

  }
}])
