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


	$scope.listMeetings = function(rel,name){
	   $scope.name = name
	   $scope.rel = rel
	   ngDialog.open({
		scope: $scope,
		template: 'meeting-list',
		controller: 'MeetingListCtrl'
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
    }

}
}])
