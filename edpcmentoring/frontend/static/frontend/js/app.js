var app = angular.module('EDPCApp', ['ngDialog'])  

// START FROM: http://django-angular.readthedocs.io/en/latest/integration.html
app.config(function($httpProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';

    //send the csrf token
    //http://stackoverflow.com/questions/18156452/django-csrf-token-angularjs
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});
app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});
// END 

app.directive("contenteditable", function() {
  return {
    restrict: "A",
    require: "ngModel",
    link: function(scope, element, attrs, ngModel) {

      function read() {
        ngModel.$setViewValue(element.html());
      }

      ngModel.$render = function() {
        element.html(ngModel.$viewValue || "");
      };

      //element.bind("blur keyup change", function() {
      element.bind("blur", function() {
        scope.$apply(read);
      });
    }
  };
});

app.controller("PreferencesFormCtrl", ['$scope', 'ngDialog', '$http', 'MemberService', '$rootScope', function ($scope,ngDialog,$http,MemberService,$rootScope){
	$scope.message = "hello world"
        $scope.me ={}

        $scope.myinvitations=[]
	$scope.invitations={}
	$rootScope.myinvs

        $scope.getMyInvitations = function(){
		if ($scope.me.id){ //fIX ME get Invitations is run be me returned!
                MemberService.myInvitations().then(function(response){
                        $scope.myinvitations = response
			$scope.invitations.myMentor = response.filter($scope.filterMentorInvite)
                        $scope.invitations.forMentor = response.filter($scope.filterInviteMentor)
			$scope.invitations.myMentee = response.filter($scope.filterMenteeInvite)
                        $scope.invitations.forMentee = response.filter($scope.filterInviteMentee)
                },function(){
                        console.log("FIXME: problems retrieving invitations")
                })
		}

	}
	
        $rootScope.$watch('myinvs',function(){
		$scope.getMyInvitations()
        })
	
        $scope.$watch('me',function(){
		//FIXME - too much processing when me is updated!
        	$scope.getMyInvitations()
        })

// call after getting 'me' $scope.getMyInvitations()

        $scope.filterMentorInvite = function(invite){
		//Invites where user is the mentor
		//return invite.created_by != $scope.me.url && invite.mentor == $scope.me.url
		console.log("created_by: "+invite.created_by.id+"  me.id: "+$scope.me.id)
		return invite.created_by.id != $scope.me.id && invite.mentor.id == $scope.me.id
	}

	
        $scope.filterInviteMentor = function(invite){
                //invites where the user has requested a mentor
                //return invite.created_by == $scope.me.url && invite.mentee == $scope.me.url
                return invite.created_by.id == $scope.me.id && invite.mentee.id == $scope.me.id
        }

        $scope.filterMenteeInvite = function(invite){
		//Invites where user is the mentee
		//return invite.created_by != $scope.me.url && invite.mentee == $scope.me.url
		return invite.created_by.id != $scope.me.id && invite.mentee.id == $scope.me.id
	}

	
        $scope.filterInviteMentee = function(invite){
                //invites where the user has requested a mentee
                //return invite.created_by == $scope.me.url && invite.mentor == $scope.me.url
                return invite.created_by.id == $scope.me.id && invite.mentor.id == $scope.me.id
        }



	//TODO: investigate a better pattern here:
	//these are used to communicate signals between controllers
	//to trigger the refresh of the lists 
	$rootScope.mentors
	$rootScope.mentees
	
        $rootScope.$watch('mentees',function(){
		$scope.updateMentees()
        })

	$scope.updateMentees = function(){
		MemberService.getMentees().then(function(response){
			$scope.mymentees = response			
		},function(){
			console.log("FIXME: problems retrieving mentees")
		})
	}
	
        $rootScope.$watch('mentors',function(){
		$scope.updateMentors()
        })

	$scope.updateMentors = function(){
		MemberService.getMentors().then(function(response){
			$scope.mymentors = response			
		},function(){
			console.log("FIXME: problems retrieving mentees")
		})
	}


        $scope.updateMe = function(newme,message){
		MemberService.updateMe(newme).then(function(response){
			$scope.me=response
		},function(){
                	alert(messge);
		});
	}

        $scope.$watch('me.mentorship_preferences.mentee_requirements',function(){
		if ($scope.me.id){ //we have set $scope.me
			$scope.updateMe($scope.me,"There was a problem updating your mentorship preferences");
		}
	})
 
        $scope.$watch('me.mentorship_preferences.mentor_requirements',function(){
		if ($scope.me.id){ //we have set $scope.me
			$scope.updateMe($scope.me,"There was a problem updating your mentorship preferences");
		}
	})
        //retrieve the users preferences
	MemberService.getMe().then(function(response) {
		$scope.me=response[0];
	},function(){
		console.log("Fixme: Problems getting current user!!");	
	})

        $scope.toggleMentorRequirements = function(){
		$scope.me.mentorship_preferences.is_seeking_mentor = !$scope.me.mentorship_preferences.is_seeking_mentor 
		$scope.updateMe($scope.me,"There was a problem updating your mentorship preferences")
	}  
        $scope.toggleMenteeRequirements = function(){
		$scope.me.mentorship_preferences.is_seeking_mentee = !$scope.me.mentorship_preferences.is_seeking_mentee 
		$scope.updateMe($scope.me,"There was a problem updating your mentorship preferences")
	} 
//}])

//app.controller("MentorsFormCtrl", ['$scope', 'ngDialog', '$http', function ($scope,ngDialog,$http){
	$scope.message = "hello world of Mentors"
        $scope.mymentors =[]
        //grab our list of mentors

		
	$scope.updateMentors()
//	MemberService.getMentors().then(function(response){
//               $scope.mymentors = response 
//	},function(error){
//                alert("There have been some problems finding your mentor records - please reload the page");
//	})

	
//	$http.get("api/mentors").success(function(data){
//                $scope.mymentors = data
//        }).error(function () {
//                alert("There have been some problems finding your mentor records - please reload the page");
//        });
        $scope.recordMentorMeeting = function(relationship){
	   //if a relationship has been provided set the select to choose this 
	   if (relationship){
		console.log("we have been sent a relationship: "+JSON.stringify(relationship));
		$scope.meeting_mentor={}
		$scope.meeting_mentor.relationship = '/api/relationships/'+relationship.id+'/' 
		$scope.meeting_mentor.name = relationship.mentor.first_name+" "+relationship.mentor.last_name 
		$scope.meeting_mentor.held_on = new Date();
	  }	
	   ngDialog.open({
		scope: $scope,
		template: 'mentor-meeting',
		controller: 'MentorMeetingCtrl'
	   });	
        }
//}])
        $scope.removeMentor = function(relationship){
	   //if a relationship has been provided set the select to choose this 
	   $scope.relationship = relationship
	   ngDialog.open({
		scope: $scope,
		template: 'rm-mentor',
		controller: 'RmMentorCtrl'
	   });	
        }
        $scope.inviteMentor = function(){
	   //if a relationship has been provided set the select to choose this
	    $scope.seekingMentee=[]
            MemberService.seekingMentee().then(function(response){
                // $rootScope.mentors = new Date() //triggers watch - should be mentorInvites
		// we need to filter from the list any existing mentee relationships and myself
		filterout=[$scope.me.id]
		$scope.mymentors.forEach(function(mentor){
			console.log("Mentor: "+JSON.stringify(mentor));
			filterout.push(mentor.mentor.id)
		})		
		console.log("filter out users: "+filterout);
		filtered=[]
		if (response.length>0){
			response.forEach(function(resp){
				if (filterout.indexOf(resp.user.id)<0){
					filtered.push(resp)
				}
			})
		}
                $scope.seekingMentee=filtered
            },function(error){
                console.log("FIXME: problems inviting mentor")
            })


 
	   ngDialog.open({
		scope: $scope,
		template: 'ls-seeking-mentee',
		controller: 'InviteMentorCtrl'
	   });	
        }




//app.controller("MenteesFormCtrl", ['$scope', 'ngDialog', '$http', function ($scope,ngDialog,$http){
	$scope.message = "hello world of Mentees"
        $scope.mymentees =[]
        //grab our list of mentors
	$scope.updateMentees()
//        MemberService.getMentees().then(function(response){
//                $scope.mymentees = response
//        },function(error){
//                alert("There have been some problems finding your mentor records - please reload the page");
//        })

//        $http.get("api/mentees").success(function(data){
//                $scope.mymentees = data
//        }).error(function () {
//                alert("There have been some problems finding your mentee records - please reload the page");
//        });
        $scope.recordMenteeMeeting = function(relationship){	
           if (relationship){
		console.log("we have been sent a relationship: "+JSON.stringify(relationship));
		$scope.meeting_mentee={}
		$scope.meeting_mentee.relationship = '/api/relationships/'+relationship.id+'/' 
		$scope.meeting_mentee.name = relationship.mentee.first_name+" "+relationship.mentee.last_name 
		$scope.meeting_mentee.held_on = new Date();
	   }	
	   ngDialog.open({
		scope: $scope,
		template: 'mentee-meeting',
		controller:  'MenteeMeetingCtrl'
	   });	
        }
        $scope.removeMentee = function(relationship){
	   //if a relationship has been provided set the select to choose this 
	   $scope.relationship = relationship
	   ngDialog.open({
		scope: $scope,
		template: 'rm-mentee',
		controller: 'RmMenteeCtrl'
	   });	
        }
        $scope.inviteMentee = function(){
	    $scope.seekingMentor=[]
	   //TODO replace this and filter in inviteMentor = function
	   //if a relationship has been provided set the select to choose this
            MemberService.seekingMentor().then(function(response){
                // $rootScope.mentors = new Date() //triggers watch - should be mentorInvites
		// we need to filter from the list any existing mentee relationships and myself
		console.log("we currently are:"+$scope.me.id)
		filterout=[$scope.me.id]
		$scope.mymentees.forEach(function(mentee){
			filterout.push(mentee.mentee.id)
		})		
		console.log("filter out users: "+filterout);
		filtered=[]
		if (response.length>0){
			response.forEach(function(resp){
				if (filterout.indexOf(resp.user.id)<0){
					filtered.push(resp)
				}
			})
		}

                // $rootScope.mentors = new Date() //triggers watch - should be mentorInvites
                $scope.seekingMentor=filtered
            },function(error){
                console.log("FIXME: problems inviting mentor")
            })

 
	   ngDialog.open({
		scope: $scope,
		template: 'ls-seeking-mentor',
		controller: 'InviteMenteeCtrl'
	   });	
        }



	$scope.listMeetings = function(rel,name){
	   $scope.name = name
	   $scope.rel = rel
	   ngDialog.open({
		scope: $scope,
		template: 'meeting-list',
		controller: 'MeetingListCtrl'
	   })
	}

	$scope.manageMyMenteeInvites = function(){
	   ngDialog.open({
		scope: $scope,
		template: 'manage-my-mentee-invites',
		controller: 'manageMyMenteeInvitesCtrl'
	   })
	
	}


	$scope.manageMyMentorInvites = function(){
	   ngDialog.open({
		scope: $scope,
		template: 'manage-my-mentor-invites',
		controller: 'manageMyMentorInvitesCtrl'
	   })
	
	}
}])

app.controller("manageMyMenteeInvitesCtrl",['$scope', '$rootScope', 'ngDialog', 'MemberService', function($scope,$rootScope,ngDialog,MemberService){
	$scope.close = function(){
		ngDialog.close()
	}
        $scope.accept = function(invite){
                //sets up a message to send to the mentor
                MemberService.acceptMentor(invite).then(function(response){
			$rootScope.myinvs = new Date() //triggers watch and invite rebuild
                        //ngDialog.close()
                },function(error){
                        console.log("FIXME: problems accepting mentee")
                })

        }

        $scope.decline = function(invite){
                //sets up a message to send to the mentor
                MemberService.declineMentor(invite).then(function(response){
			$rootScope.myinvs = new Date() //triggers watch and invite rebuild
                        //ngDialog.close()
                },function(error){
                        console.log("FIXME: problems declining mentee")
                })

        }


}])


app.controller("manageMyMentorInvitesCtrl",['$scope', '$rootScope', 'ngDialog', 'MemberService', function($scope,$rootScope,ngDialog,MemberService){
	$scope.close = function(){
		ngDialog.close()
	}
        $scope.accept = function(invite){
                //sets up a message to send to the mentor
                MemberService.acceptMentee(invite).then(function(response){
			$rootScope.myinvs = new Date() //triggers watch and invite rebuild
                        //ngDialog.close()
                },function(error){
                        console.log("FIXME: problems accepting mentee")
                })

        }

        $scope.decline = function(invite){
                //sets up a message to send to the mentor
                MemberService.declineMentee(invite).then(function(response){
			$rootScope.myinvs = new Date() //triggers watch and invite rebuild
                        //ngDialog.close()
                },function(error){
                        console.log("FIXME: problems declining mentee")
                })

        }


}])

app.controller("InviteMentorCtrl",['$scope', '$rootScope', 'ngDialog', 'MemberService', function($scope,$rootScope,ngDialog,MemberService){
        $scope.set_seeker = function(seeker){
		console.log("setting seeker")
		$scope.selected_seeker = seeker;
	}
	$scope.close = function(){
		ngDialog.close()
	}
        $scope.invite = function(mentor){
		//sets up a message to send to the mentor
		MemberService.inviteMentor(mentor).then(function(response){
			$rootScope.myinvs = new Date() //triggers watch and invite rebuild
			ngDialog.close()
		},function(error){
			console.log("FIXME: problems inviting mentor")
		})

	}
}])

app.controller("InviteMenteeCtrl",['$scope', '$rootScope', 'ngDialog', 'MemberService', function($scope,$rootScope,ngDialog,MemberService){
        $scope.set_seeker = function(seeker){
		console.log("setting seeker")
		$scope.selected_seeker = seeker;
	}

	$scope.close = function(){
		ngDialog.close()
	}
        $scope.invite = function(mentee){
		//sets up a message to send to the mentor
		MemberService.inviteMentee(mentee).then(function(response){
			$rootScope.myinvs = new Date() //triggers watch - should be menteeInvites
			ngDialog.close()
		},function(error){
			console.log("FIXME: problems inviting mentor")
		})

	}
}])



app.controller("RmMenteeCtrl",['$scope', '$rootScope', 'ngDialog', 'MemberService', function($scope,$rootScope,ngDialog,MemberService){
        $scope.closeRel = function(myrel){
		myrel.is_active=false
		MemberService.closeRel(myrel).then(function(response){
			$rootScope.mentees = new Date() //triggers watch
			ngDialog.close()
		},function(error){
			console.log("FIXME: problems removing mentee")
		})

	}

	$scope.close = function(){
		ngDialog.close()
	}
}])


app.controller("RmMentorCtrl",['$scope', '$rootScope', 'ngDialog', 'MemberService', function($scope,$rootScope,ngDialog,MemberService){
	$scope.close = function(){
		ngDialog.close()
	}
        $scope.closeRel = function(myrel){
		myrel.is_active=false
		MemberService.closeRel(myrel).then(function(response){
			$rootScope.mentors = new Date() //triggers watch
			ngDialog.close()
		},function(error){
			console.log("FIXME: problems removing mentor")
		})

	}
}])


app.controller("MeetingListCtrl",['$scope', 'ngDialog', function($scope,ngDialog){
	$scope.close = function(){
		ngDialog.close()
	}
}])

app.controller("MentorMeetingCtrl", ['$scope', 'ngDialog', '$http', '$rootScope', 'MemberService', function($scope,ngDialog,$http,$rootScope,MemberService){
	//Controls the 'modal' for registering a mentor meeting
	$scope.close = function(){
		ngDialog.close()
	}
	$scope.addMentorMeeting = function(mymeeting){
		//supply held_on field as Y-m-d
		mymeeting1 = mymeeting
		mymeeting1.held_on = (mymeeting1.held_on.toISOString().split('T'))[0]
		MemberService.addMeeting(mymeeting1).then(function(response){
			$rootScope.mentors = new Date() //triggers watch
			ngDialog.close()
		},function(error){
			console.log("FIXME: problems adding meeting")
		})
	}
}])



app.controller("MenteeMeetingCtrl", ['$scope', 'ngDialog', '$http', '$rootScope', 'MemberService', function($scope,ngDialog,$http,$rootScope,MemberService){
	//Controls the 'modal' for registering a mentee meeting
        $scope.close = function(){
                ngDialog.close()
		//some message to say that the meeting was not added?
        }
        $scope.addMenteeMeeting = function(mymeeting){
		mymeeting1 = mymeeting
		mymeeting1.held_on = (mymeeting1.held_on.toISOString().split('T'))[0]
 		MemberService.addMeeting(mymeeting1).then(function(response){
			$rootScope.mentees = new Date() //triggers watch
			ngDialog.close()
		},function(error){
			console.log("FIXME: problems adding meeting")
		})
        }
}])

app.service('MemberService', ['$http','$q',function($http, $q) {
  return {
    'getMe': function() {
      var defer = $q.defer();
      $http.get("api/current").success(function(resp){
        defer.resolve(resp);
      }).error( function(err) {
        defer.reject(err);
      });
      return defer.promise;
    }, 
    'updateMe': function(newme) {
      var defer = $q.defer();
      $http.put("api/users/"+newme.id+"/",newme).success(function(resp){
        defer.resolve(resp);
      }).error( function(err) {
        defer.reject(err);
      });
      return defer.promise;
    },   
   'getMeId': function(id) {
      var defer = $q.defer();
      $http.get().success(function(resp){
        defer.resolve(resp);
      }).error( function(err) {
        defer.reject(err);
      });
      return defer.promise;
    },
   'getMentors': function() {
      var defer = $q.defer();
      $http.get("api/mentors").success(function(resp){
        defer.resolve(resp);
      }).error( function(err) {
        defer.reject(err);
      });
      return defer.promise;
    },
   'getMentees': function() {
      var defer = $q.defer();
      $http.get("api/mentees").success(function(resp){
        defer.resolve(resp);
      }).error( function(err) {
        defer.reject(err);
      });
      return defer.promise;
    },
   'addMeeting': function(mymeeting) {
      var defer = $q.defer();
      $http.post("api/meetings/",mymeeting).success(function(resp){
        defer.resolve(resp);
      }).error( function(err) {
        defer.reject(err);
      });
      return defer.promise;
    },
    'closeRel': function(myrel) {
      var defer = $q.defer();
      $http.put("api/basicrel/"+myrel.id+"/",myrel).success(function(resp){
	defer.resolve(resp);
      }).error( function(err) {
        defer.reject(err);
      });
      return defer.promise;
    },
    'inviteMentee': function(user) {
      var defer = $q.defer();
      $http.post("api/invitations/",{mentee:user.user.url}).success(function(resp){
	defer.resolve(resp);
      }).error( function(err) {
        defer.reject(err);
      });
      return defer.promise;
    },
    'inviteMentor': function(user) {
      var defer = $q.defer();
      $http.post("api/invitations/",{mentor:user.user.url}).success(function(resp){
	defer.resolve(resp);
      }).error( function(err) {
        defer.reject(err);
      });
      return defer.promise;
    },
    'acceptMentee': function(myinvite) {
      var defer = $q.defer();
      $http.put("api/invitations/"+myinvite.id+"/",{mentor_response:'A'}).success(function(resp){
	defer.resolve(resp);
      }).error( function(err) {
        defer.reject(err);
      });
      return defer.promise;
    },
    'acceptMentor': function(myinvite) {
      var defer = $q.defer();
      myinvite.mentee_response="ACCEPT"
      $http.put("api/invitations/"+myinvite.id+"/",{mentee_response:'A'}).success(function(resp){
	defer.resolve(resp);
      }).error( function(err) {
        defer.reject(err);
      });
      return defer.promise;
    },

    'declineMentee': function(myinvite) {
      var defer = $q.defer();
      $http.put("api/invitations/"+myinvite.id+"/",{mentor_response:'D'}).success(function(resp){
	defer.resolve(resp);
      }).error( function(err) {
        defer.reject(err);
      });
      return defer.promise;
    },
    'declineMentor': function(myinvite) {
      var defer = $q.defer();
      myinvite.mentee_response="DECLINE"
      $http.put("api/invitations/"+myinvite.id+"/",{mentee_response:'D'}).success(function(resp){
	defer.resolve(resp);
      }).error( function(err) {
        defer.reject(err);
      });
      return defer.promise;
    },


    'seekingMentee': function() { //list those seeking a mentee
      var defer = $q.defer();
      $http.get("api/seekrel/?mentor=true").success(function(resp){
	defer.resolve(resp);
      }).error( function(err) {
        defer.reject(err);
      });
      return defer.promise;
    },
    'seekingMentor': function() { //list those seeking a mentor
      var defer = $q.defer();
      $http.get("api/seekrel/?mentee=true").success(function(resp){
	defer.resolve(resp);
      }).error( function(err) {
        defer.reject(err);
      });
      return defer.promise;
    },
    'myInvitations': function() { //list those seeking a mentor
      var defer = $q.defer();
      $http.get("api/myinvitations/").success(function(resp){
	defer.resolve(resp);
      }).error( function(err) {
        defer.reject(err);
      });
      return defer.promise;
    }



}
}])
