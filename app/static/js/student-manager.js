var studentManager = (function () {

  var studentHome = function() {
    $.ajax({
        method: 'get',
        url: '/api/login',
        success: function(response) {
            viewManager.render('student/home', {
                user: response.user,
                mess_data:response.details,
            }, function($view) {
                },'content');
        }
    });
  }

  var viewRegistration = function() {
    viewManager.render('student/view-registration',
    function($view) {
      $view.submitViaAjax(function (response) {
        console.log(response.registration);
        viewManager.render('calender', {
            data: response.registration,
        }, function($view) {
          console.log($view);
        },'calender');
      });
    });
  }

  var changeRegistration = function() {
     viewManager.render('/student/change-registration',
         function($view) {
            $('#date_wise').find('form').submitViaAjax(function(response) {
            if(response.success) {
            page('/student-change-registration');
            }
            else {
               $view.find('.date_wise_message').text(response.message);
            }
        })
        $('#day_wise').find('form').submitViaAjax(function(response) {
          if(response.success) {
          page('/student-change-registration');
          }
          else {
             $view.find('.day_wise_message').text(response.message);
          }
      })
      $('#month_wise').find('form').submitViaAjax(function(response) {
        if(response.success) {
        page('/student-change-registration');
        }
        else {
           $view.find('.monthly_message').text(response.message);
        }
    })
      })
  }

  var defaultMess = function() {
    $.ajax({
        method: 'get',
        url: '/api/student_defaultmess',
        success: function(res) {
            console.log(res.default_mess);
            viewManager.render('student/view-default-mess', {
                data: res.default_mess,
            }, function($view) {
                console.log($view)
              });
        }
    });
  }

  var complaints = function() {
    viewManager.render('student/complaints-form',{},
    function($view) {
            $.ajax({
              method: 'get',
              url: '/api/view-complaints',
              success: function(res) {
                  viewManager.render('student/complaints-list',
                  {
                      unresolved: res.unresolved,
                      resolved: res.resolved,
                  }, function($view) {
                          console.log($view);
                      },'complaints-list-div');
              }
            });
            $view.submitViaAjax(function (response) {
                if(response.success) {
                  page('/my-complaints')
                }
            });
      })
    }
    var cancelMeals = function() {
    viewManager.render('student/cancel-meals',
      function($view) {
        $view.submitViaAjax(
          function(response) {
            if(response.success) {
              page('/student-cancel-meals')
            }
            else {
              $view.find('.message').text(response.message);
            }
          }
        )
      })
  }
  var uncancelMeals = function() {
  viewManager.render('student/uncancel-meals',
    function($view) {
      $view.submitViaAjax(
        function(response) {
          if(response.success) {
            page('/student-uncancel-meals')
          }
          else {
            $view.find('.message').text(response.message);
          }
        }
      )
    })
}

var viewStudentBill = function() {
  viewManager.render('student/view-student-bill',
    function($view) {
      $view.submitViaAjax(
        function (response) {
          viewManager.render('/student/view-student-bill-details',{bill:response.bill},
            function($view){
              console.log($view)
            }
            ,"studentbill")}
      )});
}


  var sManager = {};
  sManager.studentHome = studentHome;
  sManager.viewRegistration = viewRegistration;
  sManager.changeRegistration = changeRegistration;
  sManager.defaultMess = defaultMess;
  sManager.complaints = complaints;
  sManager.cancelMeals = cancelMeals;
  sManager.uncancelMeals = uncancelMeals;
  sManager.viewStudentBill = viewStudentBill;
  return sManager;
})();
